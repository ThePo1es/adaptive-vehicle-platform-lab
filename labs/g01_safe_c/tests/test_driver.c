#include "g01_lab.h"
#if G01_RETEST
#include "retest-1.5-v1.h"
#else
#include "sprint-1.5-v1.h"
#endif
#include "test_support.h"

#include <stdint.h>

static int check_receive_path(uint8_t expected) {
    G01FakeMmio mmio;
    G01SpscQueue queue;
    g01_mmio_init(&mmio);
    g01_spsc_init(&queue);
    g01_mmio_inject_rx(&mmio, expected);
    mmio.status |= G01_ERROR;
    G01_CHECK(g01_driver_isr(&mmio, &queue));
    G01_CHECK(mmio.log_count == 3U);
    G01_CHECK(mmio.log[0].direction == G01_MMIO_READ);
    G01_CHECK(mmio.log[0].offset == G01_STATUS_OFFSET);
    G01_CHECK(mmio.log[0].width_bits == 32U);
    G01_CHECK(mmio.log[1].offset == G01_RX_DATA_OFFSET);
    G01_CHECK(mmio.log[1].width_bits == 32U);
    G01_CHECK(mmio.log[2].direction == G01_MMIO_WRITE);
    G01_CHECK(mmio.log[2].offset == G01_IRQ_ACK_OFFSET);
    G01_CHECK(mmio.log[2].value == G01_RX_READY);
    G01_CHECK(mmio.log[2].width_bits == 32U);
    G01_CHECK((mmio.status & G01_RX_READY) == 0U);
    G01_CHECK((mmio.status & G01_ERROR) != 0U);
    uint8_t actual = 0U;
    G01_CHECK(g01_spsc_pop(&queue, &actual));
    G01_CHECK(actual == expected);
    return 0;
}

static int check_full_queue(void) {
    G01SpscQueue queue;
    g01_spsc_init(&queue);
    for (uint8_t value = 0U; value < G01_QUEUE_STORAGE - 1U; value++) {
        G01_CHECK(g01_spsc_push(&queue, value));
    }
    G01_CHECK(!g01_spsc_push(&queue, 0xFFU));
    G01_CHECK(atomic_load_explicit(&queue.dropped, memory_order_relaxed) == 1U);
    for (uint8_t expected = 0U; expected < G01_QUEUE_STORAGE - 1U; expected++) {
        uint8_t actual = 0xFFU;
        G01_CHECK(g01_spsc_pop(&queue, &actual));
        G01_CHECK(actual == expected);
    }
    G01_CHECK(!g01_spsc_pop(&queue, &(uint8_t){0}));
    atomic_store_explicit(&queue.dropped, UINT32_MAX, memory_order_relaxed);
    for (uint8_t value = 0U; value < G01_QUEUE_STORAGE - 1U; value++) {
        G01_CHECK(g01_spsc_push(&queue, value));
    }
    G01_CHECK(!g01_spsc_push(&queue, 0xFFU));
    G01_CHECK(atomic_load_explicit(&queue.dropped, memory_order_relaxed) == UINT32_MAX);
    return 0;
}

static int check_timeout(void) {
    G01FakeMmio mmio;
    g01_mmio_init(&mmio);
    g01_mmio_inject_rx(&mmio, 0x55U);
    G01_CHECK(g01_driver_poll_ready(&mmio, 10U, 14U, 5U));
    G01_CHECK(!g01_driver_poll_ready(&mmio, 10U, 15U, 5U));
    G01_CHECK(g01_driver_poll_ready(&mmio, UINT32_MAX - 2U, 1U, 5U));
    return 0;
}

int main(void) {
    G01_CHECK(atomic_is_lock_free(&(G01SpscQueue){0}.head));
    for (size_t index = 0U; index < G01_DRIVER_RX_COUNT; index++) {
        G01_CHECK(check_receive_path(G01_DRIVER_RX_VALUES[index]) == 0);
    }
    G01_CHECK(check_timeout() == 0);
    G01_CHECK(check_full_queue() == 0);
#if G01_TESTING
    G01SpscQueue orders;
    g01_spsc_init(&orders);
    G01_CHECK(g01_spsc_push(&orders, 0x55U));
    uint8_t value = 0U;
    G01_CHECK(g01_spsc_pop(&orders, &value));
    G01_CHECK(orders.last_publish_order == memory_order_release);
    G01_CHECK(orders.last_consume_order == memory_order_acquire);
#endif
    return 0;
}
