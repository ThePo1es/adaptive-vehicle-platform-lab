#ifndef G01_SPRINT_1_2_V1_H
#define G01_SPRINT_1_2_V1_H

#include "g01_lab.h"

typedef struct {
    uint8_t low;
    uint8_t high;
    uint16_t little_endian;
} G01MemoryCase;

static const G01MemoryCase G01_MEMORY_CASES[] = {
    {0x00, 0x00, 0x0000},
    {0x34, 0x12, 0x1234},
    {0xFF, 0x7F, 0x7FFF},
    {0x00, 0x80, 0x8000},
    {0xFF, 0xFF, 0xFFFF},
};

static const size_t G01_MEMORY_CASE_COUNT = sizeof(G01_MEMORY_CASES) / sizeof(G01_MEMORY_CASES[0]);

#endif
