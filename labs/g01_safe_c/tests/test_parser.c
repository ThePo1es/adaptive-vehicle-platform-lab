#include "g01_lab.h"
#include "sprint-1.4-v1.h"
#include "test_support.h"

#include <string.h>

static uint32_t next_random(uint32_t state) {
    state ^= state << 13U;
    state ^= state >> 17U;
    state ^= state << 5U;
    return state;
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
    G01_CHECK(check_deterministic_corpus() == 0);
    return 0;
}
