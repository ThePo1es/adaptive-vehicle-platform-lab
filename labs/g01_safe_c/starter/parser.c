#include "g01_lab.h"

uint8_t g01_crc8_atm(const uint8_t *bytes, size_t length) {
    (void)bytes;
    (void)length;
    return 0U;
}

G01ParseResult g01_parse_frame(const uint8_t *bytes, size_t length) {
    (void)bytes;
    (void)length;
    return (G01ParseResult){.status = G01_PARSE_REJECTED};
}

void g01_stream_init(G01StreamParser *parser) {
    (void)parser;
}

G01ParseResult g01_stream_consume(G01StreamParser *parser, uint8_t byte) {
    (void)parser;
    (void)byte;
    return (G01ParseResult){.status = G01_PARSE_REJECTED};
}
