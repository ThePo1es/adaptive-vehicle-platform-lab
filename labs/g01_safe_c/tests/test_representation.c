#include "g01_lab.h"
#include "sprint-1.2-v1.h"
#include "test_support.h"

#include <string.h>

int main(void) {
    for (size_t index = 0U; index < G01_MEMORY_CASE_COUNT; index++) {
        const G01MemoryCase *test_case = &G01_MEMORY_CASES[index];
        for (size_t offset = 0U; offset < 8U; offset++) {
            uint8_t storage[10] = {0};
            storage[offset] = test_case->low;
            storage[offset + 1U] = test_case->high;
            G01_CHECK(g01_read_le16(&storage[offset]) == test_case->little_endian);
            uint16_t native = 0U;
            (void)memcpy(&native, &storage[offset], sizeof(native));
            G01_CHECK(g01_read_native16(&storage[offset]) == native);
        }
    }
    return 0;
}
