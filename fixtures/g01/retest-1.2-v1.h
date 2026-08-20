#ifndef G01_RETEST_1_2_V1_H
#define G01_RETEST_1_2_V1_H

#include "g01_lab.h"

typedef struct {
    uint8_t low;
    uint8_t high;
    uint16_t little_endian;
} G01MemoryCase;

static const G01MemoryCase G01_MEMORY_CASES[] = {
    {0x01, 0x02, 0x0201},
    {0xAA, 0x55, 0x55AA},
    {0xEF, 0xBE, 0xBEEF},
    {0x5A, 0xA5, 0xA55A},
};

static const size_t G01_MEMORY_CASE_COUNT = sizeof(G01_MEMORY_CASES) / sizeof(G01_MEMORY_CASES[0]);

#endif
