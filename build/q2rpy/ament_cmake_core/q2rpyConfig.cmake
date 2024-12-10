# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_q2rpy_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED q2rpy_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(q2rpy_FOUND FALSE)
  elseif(NOT q2rpy_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(q2rpy_FOUND FALSE)
  endif()
  return()
endif()
set(_q2rpy_CONFIG_INCLUDED TRUE)

# output package information
if(NOT q2rpy_FIND_QUIETLY)
  message(STATUS "Found q2rpy: 0.0.0 (${q2rpy_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'q2rpy' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${q2rpy_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(q2rpy_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${q2rpy_DIR}/${_extra}")
endforeach()
