#ifndef G01_LAB_H
#define G01_LAB_H

#include <limits.h>
#include <stdatomic.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

_Static_assert(CHAR_BIT == 8, "G1 requires 8-bit bytes");
_Static_assert(UINT8_MAX == 255U, "G1 requires uint8_t");
_Static_assert(UINT16_MAX == 65535U, "G1 requires uint16_t");

typedef struct {
    uint16_t speed_centi_kmh;
    int32_t temperature_deci_c;
    uint8_t rolling_counter;
} G01Signals;

bool g01_decode_signals(const uint8_t *payload, size_t length, G01Signals *output);
bool g01_encode_signals(const G01Signals *signals, uint8_t *payload, size_t length);
uint16_t g01_read_le16(const uint8_t *bytes);
uint16_t g01_read_native16(const uint8_t *bytes);

enum { G01_QUEUE_STORAGE = 8, G01_POOL_SLOTS = 4, G01_MAX_PAYLOAD = 16 };

typedef enum {
    G01_REJECT_NEW,
    G01_OVERWRITE_OLDEST,
} G01FullPolicy;

typedef struct {
    uint8_t values[G01_QUEUE_STORAGE];
    size_t capacity;
    size_t head;
    size_t tail;
    size_t count;
    uint32_t dropped;
    G01FullPolicy policy;
} G01Queue;

#define G01_DECLARE_QUEUE(name, capacity_value) \
    _Static_assert((capacity_value) > 0U, "queue capacity must be positive"); \
    _Static_assert((capacity_value) <= G01_QUEUE_STORAGE, "queue capacity exceeds storage"); \
    G01Queue name

bool g01_queue_init(G01Queue *queue, size_t capacity, G01FullPolicy policy);
bool g01_queue_push(G01Queue *queue, uint8_t value);
bool g01_queue_pop(G01Queue *queue, uint8_t *value);

typedef struct {
    uint8_t index;
    uint16_t generation;
} G01PoolHandle;

typedef struct {
    uint32_t values[G01_POOL_SLOTS];
    uint16_t generations[G01_POOL_SLOTS];
    bool used[G01_POOL_SLOTS];
    uint32_t rejected_releases;
} G01Pool;

void g01_pool_init(G01Pool *pool);
bool g01_pool_allocate(G01Pool *pool, G01PoolHandle *handle);
bool g01_pool_release(G01Pool *pool, G01PoolHandle handle);
uint32_t *g01_pool_value(G01Pool *pool, G01PoolHandle handle);

typedef enum {
    G01_PARSE_COMPLETE,
    G01_PARSE_NEED_MORE,
    G01_PARSE_REJECTED,
} G01ParseStatus;

typedef struct {
    G01ParseStatus status;
    size_t consumed;
    uint8_t length;
    uint8_t payload[G01_MAX_PAYLOAD];
} G01ParseResult;

typedef struct {
    uint8_t frame[3U + G01_MAX_PAYLOAD + 1U];
    size_t used;
    size_t expected;
} G01StreamParser;

uint8_t g01_crc8_atm(const uint8_t *bytes, size_t length);
G01ParseResult g01_parse_frame(const uint8_t *bytes, size_t length);
void g01_stream_init(G01StreamParser *parser);
G01ParseResult g01_stream_consume(G01StreamParser *parser, uint8_t byte);

typedef struct {
    uint8_t values[G01_QUEUE_STORAGE];
    _Atomic size_t head;
    _Atomic size_t tail;
    _Atomic uint32_t dropped;
} G01SpscQueue;

void g01_spsc_init(G01SpscQueue *queue);
bool g01_spsc_push(G01SpscQueue *queue, uint8_t value);
bool g01_spsc_pop(G01SpscQueue *queue, uint8_t *value);

typedef enum {
    G01_MMIO_READ,
    G01_MMIO_WRITE,
} G01MmioDirection;

typedef struct {
    G01MmioDirection direction;
    uint32_t offset;
    uint32_t value;
} G01MmioAccess;

enum {
    G01_STATUS_OFFSET = 0x00,
    G01_CONTROL_OFFSET = 0x04,
    G01_RX_DATA_OFFSET = 0x08,
    G01_IRQ_ACK_OFFSET = 0x0C,
    G01_RX_READY = 0x01,
    G01_ERROR = 0x02,
};

typedef struct {
    uint32_t status;
    uint32_t control;
    uint32_t rx_data;
    G01MmioAccess log[16];
    size_t log_count;
} G01FakeMmio;

void g01_mmio_init(G01FakeMmio *mmio);
void g01_mmio_inject_rx(G01FakeMmio *mmio, uint8_t value);
bool g01_driver_poll_ready(G01FakeMmio *mmio, uint32_t start, uint32_t now, uint32_t timeout);
bool g01_driver_isr(G01FakeMmio *mmio, G01SpscQueue *queue);

#endif
