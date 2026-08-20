#pragma once

#include <array>
#include <cstddef>
#include <cstdint>

namespace g02::fixture {
inline constexpr std::array<std::byte, 7> payload{
    std::byte{0xA5}, std::byte{0x00}, std::byte{0xFF}, std::byte{0x5A},
    std::byte{0xC3}, std::byte{0x3C}, std::byte{0x81},
};
inline constexpr std::uint32_t sequence = 0xFFFF'FFFEU;
}
