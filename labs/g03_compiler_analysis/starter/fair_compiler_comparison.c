typedef unsigned int u32;

u32 crc_step(u32 crc, u32 byte) {
    return crc + byte;
}
