cmake_minimum_required(VERSION 3.24)

project(g02_embedded_cpp_runtime VERSION 1.0.0 LANGUAGES C CXX)

find_package(Threads REQUIRED)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(
    G02_SOURCE_ROOT
    "${CMAKE_CURRENT_LIST_DIR}/../../labs/g02_embedded_cpp/reference"
    CACHE PATH
    "Directory containing lifetime.cpp, runtime.cpp, queue.cpp and abi.cpp"
)
set(
    G02_INCLUDE_ROOT
    "${CMAKE_CURRENT_LIST_DIR}/../../labs/g02_embedded_cpp/include"
    CACHE PATH
    "Directory containing the G2 public headers"
)

add_library(
    g02_embedded_cpp
    "${G02_SOURCE_ROOT}/lifetime.cpp"
    "${G02_SOURCE_ROOT}/runtime.cpp"
    "${G02_SOURCE_ROOT}/queue.cpp"
    "${G02_SOURCE_ROOT}/abi.cpp"
)
target_include_directories(
    g02_embedded_cpp
    PUBLIC
        "$<BUILD_INTERFACE:${G02_INCLUDE_ROOT}>"
        "$<INSTALL_INTERFACE:include>"
)
target_compile_definitions(g02_embedded_cpp PRIVATE G02_MUTANT=0 G02_TESTING=0)
target_link_libraries(g02_embedded_cpp PUBLIC Threads::Threads)

if(MSVC)
    target_compile_options(g02_embedded_cpp PRIVATE /W4 /WX)
else()
    target_compile_options(
        g02_embedded_cpp
        PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -Werror
    )
    set_source_files_properties(
        "${G02_SOURCE_ROOT}/runtime.cpp"
        "${G02_SOURCE_ROOT}/queue.cpp"
        "${G02_SOURCE_ROOT}/abi.cpp"
        PROPERTIES COMPILE_OPTIONS "-fno-exceptions;-fno-rtti"
    )
endif()

add_executable(g02_cpp_demo demo.cpp)
target_link_libraries(g02_cpp_demo PRIVATE g02_embedded_cpp)

add_executable(g02_c_demo demo_c.c)
target_link_libraries(g02_c_demo PRIVATE g02_embedded_cpp)
set_property(TARGET g02_c_demo PROPERTY LINKER_LANGUAGE CXX)

enable_testing()
add_test(NAME g02_cpp_demo COMMAND g02_cpp_demo)
add_test(NAME g02_c_demo COMMAND g02_c_demo)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(G02_PACKAGE_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/G02EmbeddedCpp")

install(
    TARGETS g02_embedded_cpp
    EXPORT G02EmbeddedCppTargets
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)
install(
    FILES
        "${G02_INCLUDE_ROOT}/g02_lifetime.hpp"
        "${G02_INCLUDE_ROOT}/g02_runtime.hpp"
        "${G02_INCLUDE_ROOT}/g02_queue.hpp"
        "${G02_INCLUDE_ROOT}/g02_abi.hpp"
        "${G02_INCLUDE_ROOT}/g02_abi_c.h"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)
install(
    EXPORT G02EmbeddedCppTargets
    FILE G02EmbeddedCppTargets.cmake
    NAMESPACE G02::
    DESTINATION "${G02_PACKAGE_DIR}"
)
configure_package_config_file(
    "${CMAKE_CURRENT_LIST_DIR}/cmake/G02EmbeddedCppConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/G02EmbeddedCppConfig.cmake"
    INSTALL_DESTINATION "${G02_PACKAGE_DIR}"
)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/G02EmbeddedCppConfigVersion.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY SameMajorVersion
)
install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/G02EmbeddedCppConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/G02EmbeddedCppConfigVersion.cmake"
    DESTINATION "${G02_PACKAGE_DIR}"
)

add_test(
    NAME g02_installed_consumer
    COMMAND
        "${CMAKE_COMMAND}"
        "-DBUILD_DIR:PATH=${CMAKE_BINARY_DIR}"
        "-DINSTALL_PREFIX:PATH=${CMAKE_BINARY_DIR}/installed-consumer-prefix"
        "-DCONSUMER_SOURCE:PATH=${CMAKE_CURRENT_LIST_DIR}/consumer"
        "-DCONSUMER_BUILD:PATH=${CMAKE_BINARY_DIR}/installed-consumer-build"
        "-DGENERATOR:STRING=${CMAKE_GENERATOR}"
        "-DGENERATOR_PLATFORM:STRING=${CMAKE_GENERATOR_PLATFORM}"
        "-DPARENT_CXX_COMPILER:FILEPATH=${CMAKE_CXX_COMPILER}"
        "-DPARENT_CXX_COMPILER_ARG1:STRING=${CMAKE_CXX_COMPILER_ARG1}"
        "-DPARENT_AR:FILEPATH=${CMAKE_AR}"
        "-DPARENT_RANLIB:FILEPATH=${CMAKE_RANLIB}"
        -P "${CMAKE_CURRENT_LIST_DIR}/cmake/verify_installed_consumer.cmake"
)
set_tests_properties(
    g02_installed_consumer
    PROPERTIES DEPENDS "g02_cpp_demo;g02_c_demo"
)
