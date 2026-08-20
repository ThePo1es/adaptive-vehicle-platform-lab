#include "g01_lab.h"
#include "sprint-1.5-v1.h"
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
    G01_CHECK(mmio.log[1].offset == G01_RX_DATA_OFFSET);
    G01_CHECK(mmio.log[2].direction == G01_MMIO_WRITE);
    G01_CHECK(mmio.log[2].offset == G01_IRQ_ACK_OFFSET);
    G01_CHECK(mmio.log[2].value == G01_RX_READY);
    G01_CHECK((mmio.status & G01_RX_READY) == 0U);
    uint8_t actual = 0U;
    G01_CHECK(g01_spsc_pop(&queue, &actual));
    G01_CHECK(actual == expected);
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
    return 0;
}
