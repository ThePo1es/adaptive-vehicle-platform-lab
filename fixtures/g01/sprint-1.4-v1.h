#ifndef G01_SPRINT_1_4_V1_H
#define G01_SPRINT_1_4_V1_H

#include "g01_lab.h"

typedef struct {
    uint8_t bytes[10];
    size_t length;
    G01ParseStatus status;
    size_t consumed;
    uint8_t payload_length;
} G01FrameCase;

static const G01FrameCase G01_FRAME_CASES[] = {
    {{0xA5, 0x01, 0x00, 0x9D}, 4, G01_PARSE_COMPLETE, 4, 0},
    {{0xA5, 0x01, 0x03, 0x10, 0x20, 0x30, 0x9E}, 7, G01_PARSE_COMPLETE, 7, 3},
    {{0xA5, 0x01, 0x03, 0x10, 0x20, 0x30, 0x00}, 7, G01_PARSE_REJECTED, 7, 0},
    {{0x00}, 1, G01_PARSE_REJECTED, 1, 0},
    {{0xA5, 0x02, 0x00}, 3, G01_PARSE_REJECTED, 1, 0},
    {{0xA5, 0x01, 0x11}, 3, G01_PARSE_REJECTED, 1, 0},
    {{0xA5, 0x01, 0x00}, 3, G01_PARSE_NEED_MORE, 3, 0},
    {{0xA5, 0x01, 0x00, 0x9D, 0xFF}, 5, G01_PARSE_REJECTED, 4, 0},
};

static const size_t G01_FRAME_CASE_COUNT = sizeof(G01_FRAME_CASES) / sizeof(G01_FRAME_CASES[0]);
static const uint8_t G01_CRC_CHECK[] = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};

#endif
