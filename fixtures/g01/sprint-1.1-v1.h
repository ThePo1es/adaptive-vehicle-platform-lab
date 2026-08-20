#ifndef G01_SPRINT_1_1_V1_H
#define G01_SPRINT_1_1_V1_H

#include "g01_lab.h"

typedef struct {
    uint8_t bytes[8];
    bool valid;
    G01Signals expected;
} G01CodecCase;

static const G01CodecCase G01_CODEC_CASES[] = {
    {{0x10, 0x27, 0xD7, 0x00, 0x03, 0, 0, 0}, true, {10000, 215, 3}},
    {{0x00, 0x00, 0x70, 0xFE, 0x00, 0, 0, 0}, true, {0, -400, 0}},
    {{0xFF, 0xFF, 0x66, 0x08, 0x0F, 0, 0, 0}, true, {65535, 2150, 15}},
    {{0x01, 0x00, 0x00, 0x80, 0x01, 0, 0, 0}, false, {0, 0, 0}},
    {{0x01, 0x00, 0x67, 0x08, 0x01, 0, 0, 0}, false, {0, 0, 0}},
    {{0x01, 0x00, 0x00, 0x00, 0xF1, 0, 0, 0}, false, {0, 0, 0}},
    {{0x01, 0x00, 0x00, 0x00, 0x01, 1, 0, 0}, false, {0, 0, 0}},
};

static const size_t G01_CODEC_CASE_COUNT = sizeof(G01_CODEC_CASES) / sizeof(G01_CODEC_CASES[0]);

#endif
