#include "g01_lab.h"
#if G01_RETEST
#include "retest-1.4-v1.h"
#else
#include "sprint-1.4-v1.h"
#endif
#include "test_support.h"

#include <string.h>

static uint32_t next_random(uint32_t state) {
    state ^= state << 13U;
    state ^= state >> 17U;
    state ^= state << 5U;
    return state;
}

static uint8_t reference_crc(const uint8_t *bytes, size_t length) {
    uint8_t remainder = 0U;
    for (size_t index = 0U; index < length; index++) {
        remainder ^= bytes[index];
        for (uint8_t bit = 0U; bit < 8U; bit++) {
            const bool top_bit = (remainder & 0x80U) != 0U;
            remainder = (uint8_t)(remainder << 1U);
            if (top_bit) {
                remainder ^= 0x07U;
            }
        }
    }
    return remainder;
}

static int check_fixed_cases(void) {
    G01_CHECK(g01_crc8_atm(G01_CRC_CHECK, sizeof(G01_CRC_CHECK)) == 0xF4U);
    for (size_t index = 0U; index < G01_FRAME_CASE_COUNT; index++) {
        const G01FrameCase *test_case = &G01_FRAME_CASES[index];
        const G01ParseResult result = g01_parse_frame(test_case->bytes, test_case->length);
        G01_CHECK(result.status == test_case->status);
        G01_CHECK(result.consumed == test_case->consumed);
        G01_CHECK(result.length == test_case->payload_length);
        if (result.status == G01_PARSE_COMPLETE) {
            G01_CHECK(memcmp(result.payload, &test_case->bytes[3], result.length) == 0);
        } else {
            G01_CHECK(result.payload[0] == 0U);
        }
    }
    return 0;
}

static int check_stream_recovery(void) {
    G01StreamParser parser;
    g01_stream_init(&parser);
    G01_CHECK(g01_stream_consume(&parser, 0xA5U).status == G01_PARSE_NEED_MORE);
    G01_CHECK(g01_stream_consume(&parser, 0x00U).status == G01_PARSE_REJECTED);
    const G01FrameCase *valid = &G01_FRAME_CASES[1];
    G01ParseResult result = {0};
    for (size_t index = 0U; index < valid->length; index++) {
        result = g01_stream_consume(&parser, valid->bytes[index]);
    }
    G01_CHECK(result.status == G01_PARSE_COMPLETE);
    G01_CHECK(result.consumed == valid->length);
    G01_CHECK(result.length == valid->payload_length);

    g01_stream_init(&parser);
    G01_CHECK(g01_stream_consume(&parser, 0xA5U).status == G01_PARSE_NEED_MORE);
    G01_CHECK(g01_stream_consume(&parser, 0xA5U).status == G01_PARSE_REJECTED);
    G01_CHECK(g01_stream_consume(&parser, 0x01U).status == G01_PARSE_NEED_MORE);
    G01_CHECK(g01_stream_consume(&parser, 0x00U).status == G01_PARSE_NEED_MORE);
    G01_CHECK(g01_stream_consume(&parser, 0x9DU).status == G01_PARSE_COMPLETE);

    g01_stream_init(&parser);
    const uint8_t bad_crc_is_magic[] = {0xA5U, 0x01U, 0x00U, 0xA5U};
    for (size_t index = 0U; index < sizeof(bad_crc_is_magic); index++) {
        result = g01_stream_consume(&parser, bad_crc_is_magic[index]);
    }
    G01_CHECK(result.status == G01_PARSE_REJECTED);
    G01_CHECK(g01_stream_consume(&parser, 0x01U).status == G01_PARSE_NEED_MORE);
    G01_CHECK(g01_stream_consume(&parser, 0x00U).status == G01_PARSE_NEED_MORE);
    G01_CHECK(g01_stream_consume(&parser, 0x9DU).status == G01_PARSE_COMPLETE);
    return 0;
}

static int check_every_valid_prefix(void) {
    uint8_t frame[3U + G01_MAX_PAYLOAD + 1U] = {0xA5U, 0x01U, G01_MAX_PAYLOAD};
    for (size_t index = 0U; index < G01_MAX_PAYLOAD; index++) {
        frame[3U + index] = (uint8_t)(index * 7U + 3U);
    }
    frame[sizeof(frame) - 1U] = reference_crc(frame, sizeof(frame) - 1U);
    G01_CHECK(frame[sizeof(frame) - 1U] == g01_crc8_atm(frame, sizeof(frame) - 1U));
    for (size_t length = 0U; length < sizeof(frame); length++) {
        const G01ParseResult result = g01_parse_frame(frame, length);
        G01_CHECK(result.status == G01_PARSE_NEED_MORE);
        G01_CHECK(result.consumed == length);
        G01_CHECK(result.length == 0U);
    }
    const G01ParseResult complete = g01_parse_frame(frame, sizeof(frame));
    G01_CHECK(complete.status == G01_PARSE_COMPLETE);
    G01_CHECK(complete.consumed == sizeof(frame));
    G01_CHECK(complete.length == G01_MAX_PAYLOAD);
    G01_CHECK(memcmp(complete.payload, &frame[3], G01_MAX_PAYLOAD) == 0);
    return 0;
}

static int check_deterministic_corpus(void) {
    uint32_t random = UINT32_C(0xC01DF00D);
    uint8_t bytes[64] = {0};
    for (size_t run = 0U; run < 100000U; run++) {
        random = next_random(random);
        const size_t length = (size_t)(random % 65U);
        for (size_t index = 0U; index < length; index++) {
            random = next_random(random);
            bytes[index] = (uint8_t)(random >> 24U);
        }
        const G01ParseResult result = g01_parse_frame(bytes, length);
        G01_CHECK(result.status <= G01_PARSE_REJECTED);
        G01_CHECK(result.consumed <= length);
        G01_CHECK(result.length <= G01_MAX_PAYLOAD);
    }
    return 0;
}

int main(void) {
    G01_CHECK(check_fixed_cases() == 0);
    G01_CHECK(check_stream_recovery() == 0);
    G01_CHECK(check_every_valid_prefix() == 0);
    G01_CHECK(check_deterministic_corpus() == 0);
    return 0;
}
