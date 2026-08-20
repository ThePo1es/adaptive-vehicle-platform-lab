#ifndef G01_RETEST_1_1_V1_H
#define G01_RETEST_1_1_V1_H

#include "g01_lab.h"

typedef struct {
    uint8_t bytes[8];
    bool valid;
    G01Signals expected;
} G01CodecCase;

static const G01CodecCase G01_CODEC_CASES[] = {
    {{0x39, 0x30, 0x00, 0x00, 0x07, 0, 0, 0}, true, {12345, 0, 7}},
    {{0xEF, 0xBE, 0xFF, 0xFF, 0x0A, 0, 0, 0}, true, {48879, -1, 10}},
    {{0x02, 0x01, 0x6F, 0xFE, 0x01, 0, 0, 0}, false, {0, 0, 0}},
    {{0x02, 0x01, 0x67, 0x08, 0x01, 0, 0, 0}, false, {0, 0, 0}},
    {{0x02, 0x01, 0x00, 0x00, 0x10, 0, 0, 0}, false, {0, 0, 0}},
    {{0x02, 0x01, 0x00, 0x00, 0x01, 0, 0, 1}, false, {0, 0, 0}},
};

static const size_t G01_CODEC_CASE_COUNT = sizeof(G01_CODEC_CASES) / sizeof(G01_CODEC_CASES[0]);

#endif
