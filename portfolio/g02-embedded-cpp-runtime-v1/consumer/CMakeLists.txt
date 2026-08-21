cmake_minimum_required(VERSION 3.24)

project(g02_installed_consumer LANGUAGES CXX)

find_package(G02EmbeddedCpp 1.0 REQUIRED CONFIG)

add_executable(g02_installed_consumer main.cpp)
target_link_libraries(g02_installed_consumer PRIVATE G02::g02_embedded_cpp)
target_compile_features(g02_installed_consumer PRIVATE cxx_std_20)
