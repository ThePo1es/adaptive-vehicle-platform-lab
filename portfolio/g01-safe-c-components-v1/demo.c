#include "g01_lab.h"

#include <stdio.h>

int main(void) {
    const uint8_t bytes[8] = {0x10U, 0x27U, 0xD7U, 0x00U, 0x03U, 0U, 0U, 0U};
    G01Signals signals = {0};
    if (!g01_decode_signals(bytes, sizeof(bytes), &signals)) {
        return 1;
    }
    if ((signals.speed_centi_kmh != 10000U) ||
        (signals.temperature_deci_c != 215) ||
        (signals.rolling_counter != 3U)) {
        return 1;
    }
    (void)printf(
        "speed=%u temperature=%ld counter=%u\n",
        (unsigned int)signals.speed_centi_kmh,
        (long int)signals.temperature_deci_c,
        (unsigned int)signals.rolling_counter
    );
    return 0;
}
