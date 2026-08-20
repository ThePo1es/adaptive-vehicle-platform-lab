#include "g01_lab.h"

void g01_mmio_init(G01FakeMmio *mmio) {
    (void)mmio;
}

void g01_mmio_inject_rx(G01FakeMmio *mmio, uint8_t value) {
    (void)mmio;
    (void)value;
}

bool g01_driver_poll_ready(G01FakeMmio *mmio, uint32_t start, uint32_t now, uint32_t timeout) {
    (void)mmio;
    (void)start;
    (void)now;
    (void)timeout;
    return false;
}

bool g01_driver_isr(G01FakeMmio *mmio, G01SpscQueue *queue) {
    (void)mmio;
    (void)queue;
    return false;
}
