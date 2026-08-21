struct ClockTable {
    int (*now)(void*) noexcept;
};

struct FixedClock {
    int value;
};

__attribute__((noinline)) int read_fixed(void* context) noexcept {
    return static_cast<FixedClock*>(context)->value;
}

extern "C" __attribute__((noinline)) int g02_manual_entry(int input) {
    FixedClock clock{input};
    constexpr ClockTable table{read_fixed};
    return table.now(&clock);
}
