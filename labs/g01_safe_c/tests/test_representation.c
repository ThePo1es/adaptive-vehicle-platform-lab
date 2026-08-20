#include "g01_lab.h"
#if G01_RETEST
#include "retest-1.2-v1.h"
#else
#include "sprint-1.2-v1.h"
#endif
#include "test_support.h"

#include <string.h>

int main(void) {
    for (size_t index = 0U; index < G01_MEMORY_CASE_COUNT; index++) {
        const G01MemoryCase *test_case = &G01_MEMORY_CASES[index];
        for (size_t offset = 0U; offset < 8U; offset++) {
            uint8_t storage[10] = {0};
            storage[offset] = test_case->low;
            storage[offset + 1U] = test_case->high;
            uint16_t little_endian = 0x55AAU;
            G01_CHECK(g01_read_le16(&storage[offset], sizeof(storage) - offset, &little_endian));
            G01_CHECK(little_endian == test_case->little_endian);
            uint16_t native = 0U;
            (void)memcpy(&native, &storage[offset], sizeof(native));
            uint16_t actual_native = 0x55AAU;
            G01_CHECK(g01_read_native16(&storage[offset], sizeof(storage) - offset, &actual_native));
            G01_CHECK(actual_native == native);
        }
    }
    const uint8_t bytes[8] = {0x34U, 0x12U};
    for (size_t length = 0U; length <= sizeof(bytes); length++) {
        uint16_t little_endian = 0xA55AU;
        uint16_t native = 0xA55AU;
        const bool expected = length >= sizeof(uint16_t);
        G01_CHECK(g01_read_le16(bytes, length, &little_endian) == expected);
        G01_CHECK(g01_read_native16(bytes, length, &native) == expected);
        if (!expected) {
            G01_CHECK(little_endian == 0xA55AU);
            G01_CHECK(native == 0xA55AU);
        }
    }
    uint16_t unchanged = 0xA55AU;
    G01_CHECK(!g01_read_le16(NULL, 2U, &unchanged));
    G01_CHECK(!g01_read_le16(bytes, 2U, NULL));
    G01_CHECK(unchanged == 0xA55AU);
    return 0;
}
