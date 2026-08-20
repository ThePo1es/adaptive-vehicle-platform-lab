#include "g01_lab.h"

bool g01_queue_init(G01Queue *queue, size_t capacity, G01FullPolicy policy) {
    (void)queue;
    (void)capacity;
    (void)policy;
    return false;
}

bool g01_queue_push(G01Queue *queue, uint8_t value) {
    (void)queue;
    (void)value;
    return false;
}

bool g01_queue_pop(G01Queue *queue, uint8_t *value) {
    (void)queue;
    (void)value;
    return false;
}

void g01_pool_init(G01Pool *pool) {
    (void)pool;
}

bool g01_pool_allocate(G01Pool *pool, G01PoolHandle *handle) {
    (void)pool;
    (void)handle;
    return false;
}

bool g01_pool_release(G01Pool *pool, G01PoolHandle handle) {
    (void)pool;
    (void)handle;
    return false;
}

uint32_t *g01_pool_value(G01Pool *pool, G01PoolHandle handle) {
    (void)pool;
    (void)handle;
    return NULL;
}

void g01_spsc_init(G01SpscQueue *queue) {
    (void)queue;
}

bool g01_spsc_push(G01SpscQueue *queue, uint8_t value) {
    (void)queue;
    (void)value;
    return false;
}

bool g01_spsc_pop(G01SpscQueue *queue, uint8_t *value) {
    (void)queue;
    (void)value;
    return false;
}
