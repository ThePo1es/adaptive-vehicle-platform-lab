typedef unsigned int u32;

__attribute__((noinline)) u32 mix4(u32 a, u32 b, u32 c, u32 d, u32 e) {
    return (a + b) ^ (c + d + e);
}

u32 call_mix4(u32 seed) {
    return mix4(seed, seed + 1U, seed + 2U, seed + 3U, seed + 4U);
}
