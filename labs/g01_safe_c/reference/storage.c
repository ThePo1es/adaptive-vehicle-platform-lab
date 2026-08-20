#include "g01_lab.h"

#include <string.h>

bool g01_queue_init(G01Queue *queue, size_t capacity, G01FullPolicy policy) {
    if ((queue == NULL) || (capacity == 0U) || (capacity > G01_QUEUE_STORAGE)) {
        return false;
    }
    *queue = (G01Queue){.capacity = capacity, .policy = policy};
    return true;
}

bool g01_queue_push(G01Queue *queue, uint8_t value) {
    if ((queue == NULL) || (queue->count > queue->capacity)) {
        return false;
    }
    if (queue->count == queue->capacity) {
        if (queue->policy == G01_REJECT_NEW) {
            queue->dropped++;
            return false;
        }
        queue->head = (queue->head + 1U) % queue->capacity;
        queue->count--;
        queue->dropped++;
    }
    queue->values[queue->tail] = value;
    queue->tail = (queue->tail + 1U) % queue->capacity;
#if G01_MUTANT == 30
    queue->count += 2U;
#else
    queue->count++;
#endif
    return true;
}

bool g01_queue_pop(G01Queue *queue, uint8_t *value) {
    if ((queue == NULL) || (value == NULL) || (queue->count == 0U)) {
        return false;
    }
    *value = queue->values[queue->head];
    queue->head = (queue->head + 1U) % queue->capacity;
    queue->count--;
    return true;
}

void g01_pool_init(G01Pool *pool) {
    *pool = (G01Pool){0};
    for (size_t index = 0U; index < G01_POOL_SLOTS; index++) {
        pool->generations[index] = 1U;
    }
}

bool g01_pool_allocate(G01Pool *pool, G01PoolHandle *handle) {
    if ((pool == NULL) || (handle == NULL)) {
        return false;
    }
    for (size_t index = 0U; index < G01_POOL_SLOTS; index++) {
        if (!pool->used[index]) {
            pool->used[index] = true;
            pool->values[index] = 0U;
            *handle = (G01PoolHandle){
                .index = (uint8_t)index,
                .generation = pool->generations[index],
            };
            return true;
        }
    }
    return false;
}

static bool g01_pool_handle_is_live(const G01Pool *pool, G01PoolHandle handle) {
    return (handle.index < G01_POOL_SLOTS) && pool->used[handle.index] &&
        (pool->generations[handle.index] == handle.generation);
}

bool g01_pool_release(G01Pool *pool, G01PoolHandle handle) {
    if ((pool == NULL) || !g01_pool_handle_is_live(pool, handle)) {
        if (pool != NULL) {
            pool->rejected_releases++;
        }
        return false;
    }
    pool->used[handle.index] = false;
#if G01_MUTANT == 31
    pool->generations[handle.index] = handle.generation;
#else
    pool->generations[handle.index] = (uint16_t)(handle.generation + 1U);
#endif
    return true;
}

uint32_t *g01_pool_value(G01Pool *pool, G01PoolHandle handle) {
    if ((pool == NULL) || !g01_pool_handle_is_live(pool, handle)) {
        return NULL;
    }
    return &pool->values[handle.index];
}

void g01_spsc_init(G01SpscQueue *queue) {
    (void)memset(queue->values, 0, sizeof(queue->values));
    atomic_init(&queue->head, 0U);
    atomic_init(&queue->tail, 0U);
    atomic_init(&queue->dropped, 0U);
}

bool g01_spsc_push(G01SpscQueue *queue, uint8_t value) {
#if G01_MUTANT == 50
    (void)value;
#endif
    const size_t tail = atomic_load_explicit(&queue->tail, memory_order_relaxed);
    const size_t next = (tail + 1U) % G01_QUEUE_STORAGE;
    const size_t head = atomic_load_explicit(&queue->head, memory_order_acquire);
    if (next == head) {
        (void)atomic_fetch_add_explicit(&queue->dropped, 1U, memory_order_relaxed);
        return false;
    }
#if G01_MUTANT == 50
    atomic_store_explicit(&queue->tail, next, memory_order_relaxed);
    queue->values[tail] = 0U;
#else
    queue->values[tail] = value;
    atomic_store_explicit(&queue->tail, next, memory_order_release);
#endif
    return true;
}

bool g01_spsc_pop(G01SpscQueue *queue, uint8_t *value) {
    const size_t head = atomic_load_explicit(&queue->head, memory_order_relaxed);
    const size_t tail = atomic_load_explicit(&queue->tail, memory_order_acquire);
    if ((head == tail) || (value == NULL)) {
        return false;
    }
    *value = queue->values[head];
    atomic_store_explicit(
        &queue->head,
        (head + 1U) % G01_QUEUE_STORAGE,
        memory_order_release
    );
    return true;
}
