#ifndef G01_RETEST_1_4_V1_H
#define G01_RETEST_1_4_V1_H

#include "g01_lab.h"

typedef struct {
    uint8_t bytes[10];
    size_t length;
    G01ParseStatus status;
    size_t consumed;
    uint8_t payload_length;
} G01FrameCase;

static const G01FrameCase G01_FRAME_CASES[] = {
    {{0xA5, 0x01, 0x01, 0x42, 0x06}, 5, G01_PARSE_COMPLETE, 5, 1},
    {{0xA5, 0x01, 0x04, 0x01, 0x02, 0x03, 0x04, 0xC4}, 8, G01_PARSE_COMPLETE, 8, 4},
    {{0xA5, 0x01, 0x01, 0x42, 0xA5}, 5, G01_PARSE_REJECTED, 5, 0},
    {{0xA5, 0x03, 0x00}, 3, G01_PARSE_REJECTED, 1, 0},
    {{0xA5, 0x01}, 2, G01_PARSE_NEED_MORE, 2, 0},
    {{0xA5, 0x01, 0x00, 0x9D, 0xA5}, 5, G01_PARSE_REJECTED, 4, 0},
};

static const size_t G01_FRAME_CASE_COUNT = sizeof(G01_FRAME_CASES) / sizeof(G01_FRAME_CASES[0]);
static const uint8_t G01_CRC_CHECK[] = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};

#endif
