struct Clock {
    virtual int now() noexcept = 0;
    virtual ~Clock() = default;
};

struct FixedClock final : Clock {
    explicit FixedClock(int value) noexcept : value{value} {}
    int now() noexcept override { return value; }
    int value;
};

extern "C" __attribute__((noinline)) int g02_virtual_entry(int input) {
    FixedClock clock{input};
    Clock* interface = &clock;
    asm volatile("" : "+r"(interface));
    return interface->now();
}
