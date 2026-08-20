#pragma once

#include <array>
#include <cstddef>
#include <cstdint>

namespace g02::fixture {
inline constexpr std::array<std::byte, 8> payload{
    std::byte{0x10}, std::byte{0x21}, std::byte{0x32}, std::byte{0x43},
    std::byte{0x54}, std::byte{0x65}, std::byte{0x76}, std::byte{0x87},
};
inline constexpr std::uint32_t sequence = 0x1020'3040U;
}
