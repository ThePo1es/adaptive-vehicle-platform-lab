typedef unsigned long u64;

static u64 recover_signal(u64 raw) {
    return raw + 7UL;
}
