#include "g02_runtime.hpp"

int main() {
    g02::EventRuntime runtime{g02::FullPolicy::RejectNewest};
    return runtime.size() == 0U ? 0 : 1;
}
