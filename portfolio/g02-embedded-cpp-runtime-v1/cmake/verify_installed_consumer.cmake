foreach(
    required
    BUILD_DIR
    INSTALL_PREFIX
    CONSUMER_SOURCE
    CONSUMER_BUILD
    GENERATOR
    PARENT_CXX_COMPILER
    PARENT_AR
)
    if(NOT DEFINED ${required} OR "${${required}}" STREQUAL "")
        message(FATAL_ERROR "missing required value: ${required}")
    endif()
endforeach()

execute_process(
    COMMAND "${CMAKE_COMMAND}" --install "${BUILD_DIR}" --prefix "${INSTALL_PREFIX}"
    RESULT_VARIABLE install_result
    OUTPUT_VARIABLE install_output
    ERROR_VARIABLE install_error
)
if(NOT install_result EQUAL 0)
    message(FATAL_ERROR "installed-consumer install failed\n${install_output}${install_error}")
endif()

set(
    configure_command
    "${CMAKE_COMMAND}"
    -S "${CONSUMER_SOURCE}"
    -B "${CONSUMER_BUILD}"
    -G "${GENERATOR}"
    "-DCMAKE_PREFIX_PATH=${INSTALL_PREFIX}"
    "-DCMAKE_CXX_COMPILER=${PARENT_CXX_COMPILER}"
    "-DCMAKE_AR=${PARENT_AR}"
)
if(DEFINED PARENT_CXX_COMPILER_ARG1 AND NOT "${PARENT_CXX_COMPILER_ARG1}" STREQUAL "")
    list(APPEND configure_command "-DCMAKE_CXX_COMPILER_ARG1=${PARENT_CXX_COMPILER_ARG1}")
endif()
if(DEFINED PARENT_RANLIB AND NOT "${PARENT_RANLIB}" STREQUAL "")
    list(APPEND configure_command "-DCMAKE_RANLIB=${PARENT_RANLIB}")
endif()
if(DEFINED GENERATOR_PLATFORM AND NOT "${GENERATOR_PLATFORM}" STREQUAL "")
    list(APPEND configure_command -A "${GENERATOR_PLATFORM}")
endif()
execute_process(
    COMMAND ${configure_command}
    RESULT_VARIABLE configure_result
    OUTPUT_VARIABLE configure_output
    ERROR_VARIABLE configure_error
)
if(NOT configure_result EQUAL 0)
    message(FATAL_ERROR "installed-consumer configure failed\n${configure_output}${configure_error}")
endif()

execute_process(
    COMMAND "${CMAKE_COMMAND}" --build "${CONSUMER_BUILD}"
    RESULT_VARIABLE build_result
    OUTPUT_VARIABLE build_output
    ERROR_VARIABLE build_error
)
if(NOT build_result EQUAL 0)
    message(FATAL_ERROR "installed-consumer build failed\n${build_output}${build_error}")
endif()
