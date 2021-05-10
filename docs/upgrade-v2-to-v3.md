# Upgrade Guide v2.3.0 --> v3.0.0

!!! caution
    **Libigl v3.0.0 is not released yet.** This page describes breaking changes and upgrade guides from our last stable release (v2.3.0) to the latest `main` branch, which will be tagged as v3.0.0 in the future. To facilitate updating, we reference the commit SHA1 that introduced each breaking changes described in this guide.

## From v2.3.0 to xxx (May 9, 2021)

!!! warning
    This entry describes changes introduced in an **unmerged** pull-request. This warning will be removed once the changes have been merged into `main`.

### CMake

#### Entry point

The main entry point for CMake is now the `CMakeLists.txt` at the root of the libigl repository. If you were using a `FindLibigl.cmake`, or were including `libigl.cmake` directly, please update your project.

If you are using the [libigl-example-project](https://github.com/libigl/libigl-example-project), you may update the content of `cmake/libigl.cmake` to the following:
```cmake
if(TARGET igl::core)
    return()
endif()

include(FetchContent)
FetchContent_Declare(
    libigl
    GIT_REPOSITORY https://github.com/libigl/libigl.git
    GIT_TAG <TARGET_SHA1>
)
FetchContent_MakeAvailable(libigl)
```

#### CMake targets

The CMake target for each libigl module has been renamed in v3.0.0. This provides greater visibility into each module category (between regular, copyleft and nonfree modules). Here is the table mapping the old names to the new names:

| Old target name (v2.3.0) | New target name (v3.0.0) |
|--------------------------|--------------------------|
| `igl::embree`            | _Unchanged_                  |
| `igl::opengl_glfw`       | `igl::glfw`                  |
| `igl::opengl_glfw_imgui` | `igl::imgui`                 |
| `igl::opengl`            | _Unchanged_                  |
| `igl::png`               | _Unchanged_                  |
| `igl::predicates`        | _Unchanged_                  |
| `igl::xml`               | _Unchanged_                  |
|                          | `igl_copyleft::core` (_New_) |
| `igl::cgal`              | `igl_copyleft::cgal`         |
| `igl::comiso`            | `igl_copyleft::comiso`       |
| `igl::cork`              | `igl_copyleft::cork`         |
| `igl::tetgen`            | `igl_copyleft::tetgen`       |
| `igl::matlab`            | `igl_nonfree::matlab`        |
| `igl::mosek`             | `igl_nonfree::mosek`         |
| `igl::triangle`          | `igl_nonfree::triangle`      |

#### CMake options

Some libigl CMake options have changed in v3.0.0. Here is a mapping from the old name to the new names:

| Old option (v2.3.0) | New option (v3.0.0) |
|---------------------|---------------------|
| LIBIGL_WITH_EMBREE            | _Unchanged_                       |
| LIBIGL_WITH_OPENGL            | _Unchanged_                       |
| LIBIGL_WITH_OPENGL_GLFW       | LIBIGL_WITH_GLFW                  |
| LIBIGL_WITH_OPENGL_GLFW_IMGUI | LIBIGL_WITH_IMGUI                 |
| LIBIGL_WITH_PNG               | _Unchanged_                       |
| LIBIGL_WITH_PREDICATES        | _Unchanged_                       |
| LIBIGL_WITH_XML               | _Unchanged_                       |
|                               | LIBIGL_COPYLEFT_WITH_CORE (_New_) |
| LIBIGL_WITH_CGAL              | LIBIGL_COPYLEFT_WITH_CGAL         |
| LIBIGL_WITH_COMISO            | LIBIGL_COPYLEFT_WITH_COMISO       |
| LIBIGL_WITH_CORK              | LIBIGL_COPYLEFT_WITH_CORK         |
| LIBIGL_WITH_TETGEN            | LIBIGL_COPYLEFT_WITH_TETGEN       |
| LIBIGL_WITH_TRIANGLE          | LIBIGL_NONFREE_WITH_TRIANGLE      |
| LIBIGL_WITH_PYTHON            | _Removed_                         |
| LIBIGL_BUILD_TESTS            | _Unchanged_                       |
| LIBIGL_BUILD_TUTORIALS        | _Unchanged_                       |
| LIBIGL_EXPORT_TARGETS         | LIBIGL_INSTALL                    |
| LIBIGL_USE_STATIC_LIBRARY     | _Unchanged_                       |

!!! tip
    There is a now a sample file `LibiglOption.cmake.sample` at the root of the libigl repository. Simply remove the `.sample` extension and edit this file to modify libigl compilation options. If you are using libigl as a subdirectory (e.g. in a parent project), then please set your options in the parent project instead.
