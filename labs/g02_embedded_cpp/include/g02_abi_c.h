#ifndef G02_ABI_C_H
#define G02_ABI_C_H

#include <stdint.h>

#ifdef __cplusplus
#define G02_NOEXCEPT noexcept
extern "C" {
#else
#define G02_NOEXCEPT
#endif

enum {
    G02_C_OK = 0,
    G02_C_INVALID_ARGUMENT = -1,
    G02_C_TIMEOUT = -2,
    G02_C_FAILED = -3,
    G02_C_NO_MEMORY = -4,
};

typedef struct G02CDependencies {
    void* context;
    int32_t (*clock_now)(void*, int32_t*) G02_NOEXCEPT;
    int32_t (*transport_send)(void*, int32_t*) G02_NOEXCEPT;
    int32_t (*launch)(void*, int32_t*) G02_NOEXCEPT;
    void (*cleanup)(void*) G02_NOEXCEPT;
} G02CDependencies;

typedef struct G02RuntimeHandle G02RuntimeHandle;

int32_t g02_runtime_create(
    const G02CDependencies* dependencies,
    G02RuntimeHandle** output) G02_NOEXCEPT;
int32_t g02_runtime_run(
    G02RuntimeHandle* handle,
    int32_t* checksum) G02_NOEXCEPT;
void g02_runtime_destroy(G02RuntimeHandle* handle) G02_NOEXCEPT;

#ifdef __cplusplus
}
#endif

#undef G02_NOEXCEPT

#endif
