#include "g02_abi_c.h"

#include <stdint.h>
#include <stdio.h>

typedef struct DemoContext {
    int cleanup_count;
} DemoContext;

static int32_t clock_now(void* context, int32_t* output) {
    (void)context;
    *output = 10;
    return G02_C_OK;
}

static int32_t transport_send(void* context, int32_t* output) {
    (void)context;
    *output = -20;
    return G02_C_OK;
}

static int32_t launch(void* context, int32_t* output) {
    (void)context;
    *output = 30;
    return G02_C_OK;
}

static void cleanup(void* context) {
    DemoContext* demo = (DemoContext*)context;
    ++demo->cleanup_count;
}

int main(void) {
    DemoContext context = {0};
    const G02CDependencies dependencies = {
        &context,
        clock_now,
        transport_send,
        launch,
        cleanup,
    };
    G02RuntimeHandle* handle = 0;
    if (g02_runtime_create(&dependencies, &handle) != G02_C_OK) {
        return 1;
    }
    int32_t checksum = 0;
    const int32_t status = g02_runtime_run(handle, &checksum);
    g02_runtime_destroy(handle);
    if (status != G02_C_OK || checksum != 20 || context.cleanup_count != 1) {
        return 2;
    }
    puts("G2 C ABI demo: PASS");
    return 0;
}
