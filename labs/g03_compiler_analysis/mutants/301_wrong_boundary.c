typedef unsigned int u32;

#define BOUNDED_STEP(value, limit) ((value) + (limit))

u32 bounded_step(u32 value, u32 limit) {
    return BOUNDED_STEP(value, limit);
}

#if G03_ORACLE
_Static_assert(BOUNDED_STEP(0U, 4U) == 1U, "first slot");
#endif
