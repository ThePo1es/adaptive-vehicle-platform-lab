#include "g01_lab.h"

#include <string.h>

bool g01_read_le16(const uint8_t *bytes, size_t length, uint16_t *output) {
    if ((bytes == NULL) || (output == NULL) || (length < 2U)) {
        return false;
    }
    const uint16_t low = bytes[0];
    const uint16_t high = bytes[1];
#if G01_MUTANT == 20
    const uint16_t value = (uint16_t)((low << 8U) | high);
#else
    const uint16_t value = (uint16_t)(low | (uint16_t)(high << 8U));
#endif
    *output = value;
    return true;
}

bool g01_read_native16(const uint8_t *bytes, size_t length, uint16_t *output) {
    if ((bytes == NULL) || (output == NULL) || (length < sizeof(*output))) {
        return false;
    }
    uint16_t value = 0U;
    (void)memcpy(&value, bytes, sizeof(value));
    *output = value;
    return true;
}

bool g01_decode_signals(const uint8_t *payload, size_t length, G01Signals *output) {
#if G01_MUTANT == 1
    (void)length;
    if ((payload == NULL) || (output == NULL)) {
#else
    if ((payload == NULL) || (output == NULL) || (length != 8U)) {
#endif
        return false;
    }
    if (((payload[4] & 0xF0U) != 0U) || (payload[5] != 0U) ||
        (payload[6] != 0U) || (payload[7] != 0U)) {
        return false;
    }
    uint16_t raw_speed = 0U;
    uint16_t raw_temperature = 0U;
    if (!g01_read_le16(payload, length, &raw_speed) ||
        !g01_read_le16(&payload[2], length - 2U, &raw_temperature)) {
        return false;
    }
    const int32_t temperature = (raw_temperature >= 0x8000U)
#if G01_MUTANT == 3
        ? (int32_t)raw_temperature - 0xFFFF
#else
        ? (int32_t)raw_temperature - 0x10000
#endif
        : (int32_t)raw_temperature;
    if ((temperature < -400) || (temperature > 2150)) {
        return false;
    }
    G01Signals decoded = {
        .speed_centi_kmh = raw_speed,
        .temperature_deci_c = temperature,
        .rolling_counter = (uint8_t)(payload[4] & 0x0FU),
    };
#if G01_MUTANT == 2
    decoded.rolling_counter = (uint8_t)(payload[4] >> 4U);
#endif
    *output = decoded;
    return true;
}

bool g01_encode_signals(const G01Signals *signals, uint8_t *payload, size_t length) {
    if ((signals == NULL) || (payload == NULL) || (length != 8U) ||
        (signals->temperature_deci_c < -400) ||
        (signals->temperature_deci_c > 2150) ||
        (signals->rolling_counter > 15U)) {
        return false;
    }
    const uint32_t temperature = (signals->temperature_deci_c < 0)
        ? (uint32_t)(signals->temperature_deci_c + 0x10000)
        : (uint32_t)signals->temperature_deci_c;
    uint8_t encoded[8] = {
        (uint8_t)(signals->speed_centi_kmh & 0xFFU),
        (uint8_t)(signals->speed_centi_kmh >> 8U),
        (uint8_t)(temperature & 0xFFU),
        (uint8_t)((temperature >> 8U) & 0xFFU),
        signals->rolling_counter,
        0U,
        0U,
        0U,
    };
#if G01_MUTANT == 4
    encoded[0] = (uint8_t)(signals->speed_centi_kmh >> 8U);
#endif
    (void)memcpy(payload, encoded, sizeof(encoded));
    return true;
}
