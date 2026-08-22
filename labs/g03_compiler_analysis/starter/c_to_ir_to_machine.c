typedef unsigned int u32;

#define BOUNDED_STEP(value, limit) ((value) + (limit))

u32 bounded_step(u32 value, u32 limit) {
    return BOUNDED_STEP(value, limit);
}

#if G03_ORACLE
_Static_assert(BOUNDED_STEP(0U, 0U) == 0U, "zero limit");
_Static_assert(BOUNDED_STEP(0U, 4U) == 1U, "first slot");
_Static_assert(BOUNDED_STEP(2U, 4U) == 3U, "middle slot");
_Static_assert(BOUNDED_STEP(3U, 4U) == 0U, "upper boundary");
_Static_assert(BOUNDED_STEP(255U, 256U) == 0U, "wide boundary");
#endif
