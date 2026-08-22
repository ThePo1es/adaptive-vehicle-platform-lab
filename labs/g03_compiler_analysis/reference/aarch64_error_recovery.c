typedef unsigned long u64;

extern u64 vehicle_scale(u64 value);

__attribute__((visibility("default"), noinline)) u64 recover_signal(u64 raw) {
    return vehicle_scale(raw) + 7UL;
}
