#include "g01_lab.h"
#include "sprint-1.3-v1.h"
#include "test_support.h"

typedef struct {
    uint8_t values[G01_QUEUE_STORAGE];
    size_t count;
    uint32_t dropped;
} QueueModel;

static uint32_t next_random(uint32_t state) {
    state ^= state << 13U;
    state ^= state >> 17U;
    state ^= state << 5U;
    return state;
}

static bool model_push(QueueModel *model, size_t capacity, G01FullPolicy policy, uint8_t value) {
    if (model->count == capacity) {
        model->dropped++;
        if (policy == G01_REJECT_NEW) {
            return false;
        }
        for (size_t index = 1U; index < model->count; index++) {
            model->values[index - 1U] = model->values[index];
        }
        model->count--;
    }
    model->values[model->count] = value;
    model->count++;
    return true;
}

static bool model_pop(QueueModel *model, uint8_t *value) {
    if (model->count == 0U) {
        return false;
    }
    *value = model->values[0];
    for (size_t index = 1U; index < model->count; index++) {
        model->values[index - 1U] = model->values[index];
    }
    model->count--;
    return true;
}

static int check_queue(G01FullPolicy policy) {
    G01Queue queue = {0};
    QueueModel model = {0};
    G01_CHECK(!g01_queue_init(&queue, 0U, policy));
    G01_CHECK(g01_queue_init(&queue, 3U, policy));
    uint32_t random = G01_STORAGE_SEED;
    for (size_t operation = 0U; operation < G01_STORAGE_MODEL_OPERATIONS; operation++) {
        random = next_random(random);
        if ((random & 1U) == 0U) {
            const uint8_t value = (uint8_t)(random >> 24U);
            G01_CHECK(g01_queue_push(&queue, value) == model_push(&model, 3U, policy, value));
        } else {
            uint8_t actual = 0xAAU;
            uint8_t expected = 0xAAU;
            G01_CHECK(g01_queue_pop(&queue, &actual) == model_pop(&model, &expected));
            G01_CHECK(actual == expected);
        }
        G01_CHECK(queue.count == model.count);
        G01_CHECK(queue.dropped == model.dropped);
        G01_CHECK(queue.count <= queue.capacity);
    }
    return 0;
}

static int check_pool(void) {
    G01Pool pool;
    g01_pool_init(&pool);
    G01PoolHandle handles[G01_POOL_SLOTS];
    for (size_t index = 0U; index < G01_POOL_SLOTS; index++) {
        G01_CHECK(g01_pool_allocate(&pool, &handles[index]));
        uint32_t *value = g01_pool_value(&pool, handles[index]);
        G01_CHECK(value != NULL);
        *value = (uint32_t)(index + 1U);
    }
    G01PoolHandle exhausted = {0};
    G01_CHECK(!g01_pool_allocate(&pool, &exhausted));
    const G01PoolHandle stale = handles[0];
    G01_CHECK(g01_pool_release(&pool, handles[0]));
    G01_CHECK(!g01_pool_release(&pool, stale));
    G01_CHECK(g01_pool_allocate(&pool, &handles[0]));
    G01_CHECK(handles[0].generation != stale.generation);
    G01_CHECK(!g01_pool_release(&pool, stale));
    const G01PoolHandle foreign = {.index = 99U, .generation = 1U};
    G01_CHECK(!g01_pool_release(&pool, foreign));
    return 0;
}

int main(void) {
    G01_CHECK(check_queue(G01_REJECT_NEW) == 0);
    G01_CHECK(check_queue(G01_OVERWRITE_OLDEST) == 0);
    G01_CHECK(check_pool() == 0);
    return 0;
}
