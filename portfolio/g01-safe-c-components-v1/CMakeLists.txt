cmake_minimum_required(VERSION 3.24)

project(g01_safe_c_components VERSION 1.0.0 LANGUAGES C)

option(G01_ZIG_DRIVER "Use the Zig executable as both the C driver and archive tool" OFF)
if(G01_ZIG_DRIVER)
    set(CMAKE_AR "${CMAKE_C_COMPILER}")
    set(CMAKE_C_ARCHIVE_CREATE "<CMAKE_AR> ar qc <TARGET> <LINK_FLAGS> <OBJECTS>")
    set(CMAKE_C_ARCHIVE_FINISH "<CMAKE_AR> ranlib <TARGET>")
endif()

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

set(
    G01_SOURCE_ROOT
    "${CMAKE_CURRENT_LIST_DIR}/../../labs/g01_safe_c/reference"
    CACHE PATH
    "Directory containing the learner's codec.c, storage.c, parser.c and driver.c"
)
set(
    G01_INCLUDE_ROOT
    "${CMAKE_CURRENT_LIST_DIR}/../../labs/g01_safe_c/include"
    CACHE PATH
    "Directory containing g01_lab.h"
)

add_library(
    g01_safe_c
    "${G01_SOURCE_ROOT}/codec.c"
    "${G01_SOURCE_ROOT}/storage.c"
    "${G01_SOURCE_ROOT}/parser.c"
    "${G01_SOURCE_ROOT}/driver.c"
)
target_include_directories(
    g01_safe_c
    PUBLIC
        "$<BUILD_INTERFACE:${G01_INCLUDE_ROOT}>"
        "$<INSTALL_INTERFACE:include>"
)
target_compile_definitions(g01_safe_c PRIVATE G01_MUTANT=0 G01_TESTING=0)

if(MSVC)
    target_compile_options(g01_safe_c PRIVATE /W4 /WX)
else()
    target_compile_options(
        g01_safe_c
        PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -Werror
    )
endif()

add_executable(g01_safe_c_demo demo.c)
target_link_libraries(g01_safe_c_demo PRIVATE g01_safe_c)

enable_testing()
add_test(NAME g01_safe_c_demo COMMAND g01_safe_c_demo)

include(GNUInstallDirs)
install(TARGETS g01_safe_c ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}")
install(FILES "${G01_INCLUDE_ROOT}/g01_lab.h" DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}")
