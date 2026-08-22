#ifndef G01_TEST_SUPPORT_H
#define G01_TEST_SUPPORT_H

#include <stdio.h>

#define G01_CHECK(condition) \
    do { \
        if (!(condition)) { \
            (void)fprintf(stderr, "check failed at %s:%d: %s\n", __FILE__, __LINE__, #condition); \
            return 1; \
        } \
    } while (0)

#endif
