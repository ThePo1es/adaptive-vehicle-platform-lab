#include "g01_lab.h"

uint16_t g01_read_le16(const uint8_t *bytes) {
    (void)bytes;
    return 0U;
}

uint16_t g01_read_native16(const uint8_t *bytes) {
    (void)bytes;
    return 0U;
}

bool g01_decode_signals(const uint8_t *payload, size_t length, G01Signals *output) {
    (void)payload;
    (void)length;
    (void)output;
    return false;
}

bool g01_encode_signals(const G01Signals *signals, uint8_t *payload, size_t length) {
    (void)signals;
    (void)payload;
    (void)length;
    return false;
}
