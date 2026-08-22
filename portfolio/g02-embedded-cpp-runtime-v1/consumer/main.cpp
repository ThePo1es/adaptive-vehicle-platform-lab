#include "g02_runtime.hpp"

#include <cstdio>

int main() {
    g02::EventRuntime runtime{g02::FullPolicy::RejectNewest};
    if (runtime.size() != 0U) {
        return 1;
    }
    std::puts("G2 installed consumer: PASS");
    return 0;
}
