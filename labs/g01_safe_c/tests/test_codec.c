#include "g01_lab.h"
#include "sprint-1.1-v1.h"
#include "test_support.h"

#include <string.h>

int main(void) {
    for (size_t index = 0U; index < G01_CODEC_CASE_COUNT; index++) {
        const G01CodecCase *test_case = &G01_CODEC_CASES[index];
        G01Signals actual = {0xAA55U, -1234, 0x0EU};
        const G01Signals before = actual;
        const bool decoded = g01_decode_signals(test_case->bytes, 8U, &actual);
        G01_CHECK(decoded == test_case->valid);
        if (test_case->valid) {
            G01_CHECK(actual.speed_centi_kmh == test_case->expected.speed_centi_kmh);
            G01_CHECK(actual.temperature_deci_c == test_case->expected.temperature_deci_c);
            G01_CHECK(actual.rolling_counter == test_case->expected.rolling_counter);
            uint8_t encoded[8] = {0};
            G01_CHECK(g01_encode_signals(&actual, encoded, sizeof(encoded)));
            G01_CHECK(memcmp(encoded, test_case->bytes, sizeof(encoded)) == 0);
        } else {
            G01_CHECK(memcmp(&actual, &before, sizeof(actual)) == 0);
        }
    }
    for (size_t length = 0U; length < 8U; length++) {
        G01Signals actual = {0xAA55U, -1234, 0x0EU};
        const G01Signals before = actual;
        G01_CHECK(!g01_decode_signals(G01_CODEC_CASES[0].bytes, length, &actual));
        G01_CHECK(memcmp(&actual, &before, sizeof(actual)) == 0);
    }
    G01_CHECK(!g01_decode_signals(NULL, 8U, NULL));
    return 0;
}
