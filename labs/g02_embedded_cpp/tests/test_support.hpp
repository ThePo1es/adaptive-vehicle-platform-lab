#pragma once

#include <cstdio>

#define G02_CHECK(condition)                                                        \
    do {                                                                            \
        if (!(condition)) {                                                          \
            std::fprintf(stderr, "CHECK failed: %s at %s:%d\n", #condition,       \
                         __FILE__, __LINE__);                                        \
            return 1;                                                               \
        }                                                                           \
    } while (false)
