#include "g01_lab.h"

static void g01_log(
    G01FakeMmio *mmio,
    G01MmioDirection direction,
    uint32_t offset,
    uint32_t value
) {
    if (mmio->log_count < (sizeof(mmio->log) / sizeof(mmio->log[0]))) {
        mmio->log[mmio->log_count] = (G01MmioAccess){
            .direction = direction,
            .offset = offset,
            .value = value,
        };
        mmio->log_count++;
    }
}

static uint32_t g01_mmio_read(G01FakeMmio *mmio, uint32_t offset) {
    uint32_t value = 0U;
    switch (offset) {
        case G01_STATUS_OFFSET:
            value = mmio->status;
            break;
        case G01_CONTROL_OFFSET:
            value = mmio->control;
            break;
        case G01_RX_DATA_OFFSET:
            value = mmio->rx_data;
            break;
        case G01_IRQ_ACK_OFFSET:
            value = 0U;
            break;
        default:
            value = 0U;
            break;
    }
    g01_log(mmio, G01_MMIO_READ, offset, value);
    return value;
}

static void g01_mmio_write(G01FakeMmio *mmio, uint32_t offset, uint32_t value) {
    g01_log(mmio, G01_MMIO_WRITE, offset, value);
    switch (offset) {
        case G01_CONTROL_OFFSET:
            mmio->control = value & 0x03U;
            break;
        case G01_IRQ_ACK_OFFSET:
            if ((value & G01_RX_READY) != 0U) {
                mmio->status &= ~((uint32_t)G01_RX_READY);
            }
            break;
        default:
            break;
    }
}

void g01_mmio_init(G01FakeMmio *mmio) {
    *mmio = (G01FakeMmio){0};
}

void g01_mmio_inject_rx(G01FakeMmio *mmio, uint8_t value) {
    mmio->rx_data = value;
    mmio->status |= G01_RX_READY;
}

bool g01_driver_poll_ready(G01FakeMmio *mmio, uint32_t start, uint32_t now, uint32_t timeout) {
#if G01_MUTANT == 52
    if (now > (start + timeout)) {
#else
    if ((uint32_t)(now - start) >= timeout) {
#endif
        return false;
    }
    return (g01_mmio_read(mmio, G01_STATUS_OFFSET) & G01_RX_READY) != 0U;
}

bool g01_driver_isr(G01FakeMmio *mmio, G01SpscQueue *queue) {
    const uint32_t status = g01_mmio_read(mmio, G01_STATUS_OFFSET);
    if ((status & G01_RX_READY) == 0U) {
        return false;
    }
    const uint8_t value = (uint8_t)(g01_mmio_read(mmio, G01_RX_DATA_OFFSET) & 0xFFU);
    const bool pushed = g01_spsc_push(queue, value);
#if G01_MUTANT == 51
    g01_mmio_write(mmio, G01_IRQ_ACK_OFFSET, status | G01_RX_READY);
#else
    g01_mmio_write(mmio, G01_IRQ_ACK_OFFSET, G01_RX_READY);
#endif
    return pushed;
}
