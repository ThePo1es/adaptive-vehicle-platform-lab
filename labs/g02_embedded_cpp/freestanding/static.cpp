template <typename Clock>
__attribute__((noinline)) int read_clock(Clock& clock) noexcept {
    return clock.now();
}

struct FixedClock {
    int now() noexcept { return value; }
    int value;
};

extern "C" __attribute__((noinline)) int g02_static_entry(int input) {
    FixedClock clock{input};
    return read_clock(clock);
}
