#include "g01_lab.h"
#if G01_RETEST
#include "retest-1.1-v1.h"
#else
#include "sprint-1.1-v1.h"
#endif
#include "test_support.h"

static bool signals_equal(const G01Signals *left, const G01Signals *right) {
    return (left->speed_centi_kmh == right->speed_centi_kmh) &&
        (left->temperature_deci_c == right->temperature_deci_c) &&
        (left->rolling_counter == right->rolling_counter);
}

static int check_round_trips(void) {
    for (uint32_t speed = 0U; speed <= UINT16_MAX; speed += 257U) {
        for (int32_t temperature = -400; temperature <= 2150; temperature += 17) {
            for (uint8_t counter = 0U; counter <= 15U; counter++) {
                const G01Signals expected = {
                    .speed_centi_kmh = (uint16_t)speed,
                    .temperature_deci_c = temperature,
                    .rolling_counter = counter,
                };
                uint8_t bytes[8] = {0};
                G01_CHECK(g01_encode_signals(&expected, bytes, sizeof(bytes)));
                G01Signals actual = {0};
                G01_CHECK(g01_decode_signals(bytes, sizeof(bytes), &actual));
                G01_CHECK(signals_equal(&actual, &expected));
            }
        }
    }
    return 0;
}

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
            for (size_t byte = 0U; byte < sizeof(encoded); byte++) {
                G01_CHECK(encoded[byte] == test_case->bytes[byte]);
            }
        } else {
            G01_CHECK(signals_equal(&actual, &before));
        }
    }
    for (size_t length = 0U; length < 8U; length++) {
        G01Signals actual = {0xAA55U, -1234, 0x0EU};
        const G01Signals before = actual;
        G01_CHECK(!g01_decode_signals(G01_CODEC_CASES[0].bytes, length, &actual));
        G01_CHECK(signals_equal(&actual, &before));
    }
    G01_CHECK(!g01_decode_signals(NULL, 8U, NULL));
    G01_CHECK(check_round_trips() == 0);
    return 0;
}
