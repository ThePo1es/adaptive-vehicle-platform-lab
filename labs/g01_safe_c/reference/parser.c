#include "g01_lab.h"

#include <string.h>

enum { G01_MAGIC = 0xA5, G01_VERSION = 0x01, G01_HEADER_SIZE = 3 };

uint8_t g01_crc8_atm(const uint8_t *bytes, size_t length) {
    uint8_t crc = 0U;
    for (size_t index = 0U; index < length; index++) {
        crc ^= bytes[index];
        for (uint8_t bit = 0U; bit < 8U; bit++) {
            crc = ((crc & 0x80U) != 0U)
                ? (uint8_t)((uint8_t)(crc << 1U) ^ 0x07U)
                : (uint8_t)(crc << 1U);
        }
    }
    return crc;
}

static G01ParseResult g01_result(G01ParseStatus status, size_t consumed) {
#if G01_MUTANT == 43
    if (status != G01_PARSE_COMPLETE) {
        return (G01ParseResult){
            .status = status,
            .consumed = consumed,
            .length = 1U,
            .payload = {0xAA},
        };
    }
#endif
    return (G01ParseResult){.status = status, .consumed = consumed};
}

G01ParseResult g01_parse_frame(const uint8_t *bytes, size_t length) {
    if ((bytes == NULL) || (length == 0U)) {
        return g01_result(G01_PARSE_NEED_MORE, 0U);
    }
    if (bytes[0] != G01_MAGIC) {
        return g01_result(G01_PARSE_REJECTED, 1U);
    }
    if (length < G01_HEADER_SIZE) {
        return g01_result(G01_PARSE_NEED_MORE, length);
    }
    if ((bytes[1] != G01_VERSION) || (bytes[2] > G01_MAX_PAYLOAD)) {
        return g01_result(G01_PARSE_REJECTED, 1U);
    }
    const size_t frame_length = G01_HEADER_SIZE + (size_t)bytes[2] + 1U;
    if (length < frame_length) {
        return g01_result(G01_PARSE_NEED_MORE, length);
    }
#if G01_MUTANT == 40
    if (g01_crc8_atm(bytes, frame_length - 2U) != bytes[frame_length - 1U]) {
#else
    if (g01_crc8_atm(bytes, frame_length - 1U) != bytes[frame_length - 1U]) {
#endif
        return g01_result(G01_PARSE_REJECTED, frame_length);
    }
#if G01_MUTANT == 41
    if (length < frame_length) {
#else
    if (length != frame_length) {
#endif
        return g01_result(G01_PARSE_REJECTED, frame_length);
    }
    G01ParseResult result = {
        .status = G01_PARSE_COMPLETE,
        .consumed = frame_length,
        .length = bytes[2],
    };
    (void)memcpy(result.payload, &bytes[G01_HEADER_SIZE], result.length);
    return result;
}

void g01_stream_init(G01StreamParser *parser) {
    *parser = (G01StreamParser){0};
}

static void g01_stream_restart(G01StreamParser *parser, uint8_t byte) {
    g01_stream_init(parser);
    if (byte == G01_MAGIC) {
        parser->frame[0] = byte;
        parser->used = 1U;
    }
}

G01ParseResult g01_stream_consume(G01StreamParser *parser, uint8_t byte) {
    if (parser->used == 0U) {
        if (byte != G01_MAGIC) {
            return g01_result(G01_PARSE_REJECTED, 1U);
        }
        parser->frame[0] = byte;
        parser->used = 1U;
        return g01_result(G01_PARSE_NEED_MORE, 1U);
    }
    if ((parser->used == 1U) && (byte != G01_VERSION)) {
        g01_stream_restart(parser, byte);
        return g01_result(G01_PARSE_REJECTED, 1U);
    }
    if ((parser->used == 2U) && (byte > G01_MAX_PAYLOAD)) {
        g01_stream_restart(parser, byte);
        return g01_result(G01_PARSE_REJECTED, 1U);
    }
    parser->frame[parser->used] = byte;
    parser->used++;
    if (parser->used == G01_HEADER_SIZE) {
        parser->expected = G01_HEADER_SIZE + (size_t)byte + 1U;
    }
    if ((parser->expected == 0U) || (parser->used < parser->expected)) {
        return g01_result(G01_PARSE_NEED_MORE, 1U);
    }
    G01ParseResult result = g01_parse_frame(parser->frame, parser->used);
#if G01_MUTANT == 42
    result.consumed++;
#endif
#if G01_MUTANT == 44
    g01_stream_init(parser);
#else
    if (result.status == G01_PARSE_REJECTED) {
        g01_stream_restart(parser, byte);
    } else {
        g01_stream_init(parser);
    }
#endif
    return result;
}
