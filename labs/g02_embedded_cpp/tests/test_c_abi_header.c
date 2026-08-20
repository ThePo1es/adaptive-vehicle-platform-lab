#include "g02_abi_c.h"

_Static_assert(G02_C_OK == 0, "success code must stay zero");
_Static_assert(G02_C_TIMEOUT < 0, "errors must stay negative");

int g02_c_header_smoke(G02CDependencies* dependencies) {
    G02RuntimeHandle* handle = 0;
    return g02_runtime_create(dependencies, &handle);
}
