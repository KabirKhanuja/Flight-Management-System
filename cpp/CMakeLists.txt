cmake_minimum_required(VERSION 3.10)
project(FlightFMS LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

file(GLOB SRC_FILES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

set(LIB_SOURCES ${SRC_FILES})
list(REMOVE_ITEM LIB_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/FMS.cpp")

if(LIB_SOURCES)
    add_library(flight_fms STATIC ${LIB_SOURCES})
    target_include_directories(flight_fms PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
    target_compile_options(flight_fms PRIVATE -O3)
endif()

add_executable(fms_app "${CMAKE_CURRENT_SOURCE_DIR}/FMS.cpp")
target_include_directories(fms_app PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
if(TARGET flight_fms)
    target_link_libraries(fms_app PRIVATE flight_fms)
endif()
target_compile_options(fms_app PRIVATE -O3)