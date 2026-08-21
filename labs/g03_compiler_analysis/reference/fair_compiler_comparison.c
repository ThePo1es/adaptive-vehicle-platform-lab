typedef unsigned int u32;

u32 crc_step(u32 crc, u32 byte) {
    crc ^= byte;
    for (u32 bit = 0U; bit < 8U; ++bit) {
        u32 const mask = 0U - (crc & 1U);
        crc = (crc >> 1U) ^ (0xEDB88320U & mask);
    }
    return crc;
}
