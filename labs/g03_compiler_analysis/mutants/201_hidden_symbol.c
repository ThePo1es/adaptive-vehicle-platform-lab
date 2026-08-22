typedef unsigned long u64;

static u64 vehicle_scale(u64 value) {
    return value;
}

static u64 recover_signal(u64 raw) {
    return vehicle_scale(raw) + 7UL;
}
