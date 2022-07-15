# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_itof_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED itof_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(itof_FOUND FALSE)
  elseif(NOT itof_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(itof_FOUND FALSE)
  endif()
  return()
endif()
set(_itof_CONFIG_INCLUDED TRUE)

# output package information
if(NOT itof_FIND_QUIETLY)
  message(STATUS "Found itof: 0.0.0 (${itof_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'itof' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${itof_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(itof_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${itof_DIR}/${_extra}")
endforeach()
