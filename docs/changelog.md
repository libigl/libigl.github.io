<!-- Hide h3+ from toc  -->
<style>.md-nav--secondary .md-nav__list .md-nav__list { display: none }</style>

# Changelog

## Summary Table

??? abstract "Click to unroll."

      Version | Short description
      --------|----------------------------------------------------------------------
      master  | DDM skinning, Bézier, PLY reader, 3D text rendering, matcap
      2.2.0   | New python bindings, fast winding number for soups, ICP algorithm
      2.1.0   | Various improvements and bug fixes, updated dependencies
      2.0.0   | Lighter, simpler CMake build, rewritten history
      1.3.3   | Switched the build system from submodules to CMake external projects
      1.3.2   | After merging PRs in the 2018 hackaton
      1.3.1   | Before merging PRs in the 2018 hackaton
      1.3.0   | Modernized cmake build, multi-mesh viewer, replace nanogui with imgui
      1.2.1   | Reorganization opengl-dependent functions: opengl and opengl2 extras
      1.2.0   | Reorganization of "extras", rm deprecated funcs, absorb boost & svd3x3
      1.1.7   | Switch build for static library to cmake.
      1.1.6   | Major boolean robustness fix, drop CGAL dependency for AABB/distances
      1.1.5   | Bug fix in booleans
      1.1.4   | Edge collapsing and linear program solving
      1.1.3   | Bug fixes in active set and boundary_conditions
      1.1.1   | PLY file format support
      1.1.0   | Mesh boolean operations using CGAL and cork, implementing [Attene 14]
      1.0.3   | Bone heat method
      1.0.2   | Bug fix in winding number code
      1.0.1   | Bug fixes and more CGAL support
      1.0.0   | Major beta release: many renames, tutorial, triangle, org. build
      0.4.6   | Generalized Winding Numbers
      0.4.5   | CGAL extra: mesh selfintersection
      0.4.4   | STL file format support
      0.4.3   | ARAP implementation
      0.4.1   | Migrated much of the FAST code including extra for Sifakis' 3x3 svd
      0.4.0   | Release under MPL2 license
      0.3.7   | Embree2.0 support
      0.3.6   | boost extra, patches, mosek 7 support, libiglbbw (mosek optional)
      0.3.5   | More examples, naive primitive sorting
      0.3.3   | Many more examples, ambient occlusion with Embree.
      0.3.1   | Linearly dependent constraints in min_quad_with_fixed, SparseQR buggy
      0.3.0   | Better active set method support
      0.2.3   | More explicits, active set method, opengl/anttweakbar guards
      0.2.2   | More explicit instantiations, faster sorts and uniques
      0.2.1   | Bug fixes in barycenter and doublearea found by Martin Bisson
      0.2.0   | XML serializer more stable and fixed bug in remove_duplicate_vertices
      0.1.8   | Embree and xml (windows only) extras
      0.1.5   | Compilation on windows, bug fix for compilation with cygwin
      0.1.1   | Alpha release with core functions, extras, examples

## Upcoming version (`master` branch)

#### New Features
- Direct Delta Mush skinning (#1541)
- New exploded view tutorial (#1510)
- Bézier curve evaluation (`igl::bezier`) and fitting (`igl::fit_cubic_bezier`) (#1476)
- Replace .ply reader/writer with tinyply library (#1422)
- `igl::copyleft::cgal::wire_mesh` now support per-edge thickness. Adds `igl::copyleft::cgal::coplanar` test (#1488)
- New generic function for connected components (`igl::connected_components`) (#1487)
- Viewer: matcap support (#1482)
- Viewer: option for double-sided lighting (#1480)
- Viewer: new 3D text rendering feature, supporting proper label depth (#1549)

#### Build System
- Update ImGui to 1.76 (#1545)

#### Misc
- Fix align_camera_center in Viewer::init() for multiple cores (#1349)
- Add floating point exceptions in unit tests (#1001)
- Extended serialization functionality to Eigen::Array (#1113)
- SCAF: Expose linear system to be solved by user code (#1553)
- Fix issue with `igl::heat_geodesic` (#1497)
- Refactored `igl::is_edge_manifold` (#1509)
- Various bugfixes, compile fixes, template fixes (#1335, #1361, #1400, #1402, #1430, #1438, #1441, #1471, #1475, #1484, #1494, #1495, #1497, #1525, #1538, #1544, #1546, #1581, #1582)

## Version 2.2.0 Changes

#### Python Bindings
The python bindings have been moved to a [separate repository](https://github.com/libigl/libigl-python-bindings). These are now available as an [conda package](https://anaconda.org/conda-forge/igl).

#### New Features
- Fast winding number for triangle soups (#1218)
- Iterative closest point algorithm + tutorial (#1347)
- Ear clipping triangulation (#1169)
- Added `igl::path_to_edges` function (#1259)
- `igl::dijkstra` can now use mesh edge length (#1170)
- Keep reference to multiple material when reading obj (#1280)
- Added `igl::sharp_edges` for sharp edges extraction (#1364)
- Added `igl::unproject_on_line`, `igl::unproject_on_plane` and `igl::projection_constraint` to compute cursor (un)-projections (#1368)
- Added `igl::quad_grid` and `igl::triangulated_grid` to create meshes from regular grids (#1369)
- Added `igl::isolines_map`, `ViewerData::set_data` and `ViewerData::set_colormap` to improve scalar field visualization in the Viewer, and updated tutorials accordingly (#1371)
- Added new `COLOR_MAP_TYPE_TURBO` colormap, based on [Turbo](https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html). Jet is now an alias for Turbo, and switched to Viridis as default colormap in the viewer (#1372)
- Added `igl::slice_sorted` and removed deprecated `Eigen::DynamicSparsematrix` from `igl::slice` (#1370)

#### Build System
- Overhauled function signatures in preparation of new python bindings (#1162, #1228, #1271, #1274)
- Added a conda environment `cmake/libigl-cgal.yml` to provide boost for Windows users (#1239)
- Added experimental support for Hunter (#1242)
- Now `libigl.cmake` will define a CMake target `Eigen3::Eigen` if not provided by the user (#1299)
- Added `igl_set_folders()` to sort CMake targets into folders in IDEs such as Visual Studio or Xcode (#1383)
- Minor fixes to our CMake build system (#1363)
- Github actions for CI replacing appveyor and travis (#1389)

#### Misc
- Fix underflow issue when computing normalization in `igl::heat_geodesics` (#1344) 
- Update nrosy to match the MIQ paper (#1303)
- Delete `Embree_convenience.h` (#1314)
- Refactored `igl::cut_mesh` (#1332)
- Various improvements to the viewer (#1196, #1251, #1366)
- Unit tests: cleand up `test_common.h` (#1365)
- Made call to `igl::predicates::exactinit()` thread-safe + marked internal functions in `predicates.c` as `static` to prevent name collisions (#1377)
- Doc cleanup (#1376)
- Allows `igl::hsv_to_rgb` to work on negative hues (#1399)
- Explicitly marked the following functions as deprecated (#1380):
    - `igl::all_edges`
    - `igl::internal_angles_using_edge_lengths` (only a specific overload is affected)
    - `igl::is_border_vertex` (only a specific overload is affected)
    - `igl::remove_duplicates`
- Various bugfixes, code cleanup and explicit template instantiations (#1197, #1210, #1216, #1231, #1247, #1258, #1288, #1309, #1320, #1337, #1345, #1379, #1396, #1327)

## Version 2.1.0 Changes

- Various code cleanup, compilation fixes, and explicit template instantiations
- Added wrapper around Shewchuk's predicates (#1163)
- libigl now also compiles with Eigen 3.3 (#1110).
- Extended `igl::cat` functionalities (#1108)
- Extended `boundary_facets` with outputs revealing which element facet comes from (#1067)
- Use `std::shuffle` instead of `std::random_shuffle` in `igl/randperm` (#1062)
- Fixed an Eigen alignment issue in the viewer (#1029)
- Removed LIM tutorial (#1012, #1014)
- Fixed current python bindings (#1008)
- Intrinsic Delaunay triangulation (#988)
- New Heat Geodesics feature (#988, #1140). See also tutorial 716.
- Switched from Google Test to Catch2 (#961), and added various unit tests
- Fixed an issue with transparent window on macOS that was introduced in v2.0.0 (#953)
- Updated dependencies: Embree 3 (#947), GLFW (#977, #1153), ImGui (#1039), std-image (#1072)
- Added sparse voxel grids (#937, #942) and tutorial 715 for meshing implicit functions.
- Added tutorial 714 for marching tets (#716)

## Version 2.0.0 Changes

This release is a result of the 2018 libigl hackathon at NYU. The major changes are:

- a simplified cmake set up that can build a static library, tutorials, tests, and python bindings;
 - cmake now uses `ExternalProject_Add` to download necessary/requested dependency source code and tutorial/test data
 - as a result, `git clone --recursive ...` is no longer required 
- unit tests are now part of main repo and included in continuous integration (https://github.com/libigl/libigl-unit-tests is obsolete);
- tutorial data has been moved to <https://github.com/libigl/libigl-tutorial-data>;
- unit test data has been moved to <https://github.com/libigl/libigl-tests-data>;
- all dependencies previously in `libigl/external` have been removed or moved to repos (and added via `ExternalProject_Add`);
- documentation and the tutorial webpage has been moved to <https://github.com/libigl/libigl.github.io>;
- .git history of these files has been _**purged**_ using [bfg](https://rtyley.github.io/bfg-repo-cleaner/)
- unfortunately this means that SHA hashes have changed and any external projects using libigl as a _submodule_ will need to be refreshed to the new hashes.
- More information and instructions for troubleshooting at <https://libigl.github.io/rewritten-history/>.
- A legacy version with SHA hashes matching old repo is hosted at https://github.com/libigl/libigl-legacy.

The **major upshot** is that the old `git clone --recursive` that resulted in a 1.8GB `libigl/` directory is now a `git clone ` that results in 16.5MB, more than a **100x** reduction in size. 

Name changes:

Old                                     | New
--------------------------------------- | -----------------------------------
`igl::components`                       | `igl::vertex_components`
`igl::slice_tets`                       | `igl::marching_tets`

## Version 1.3.2 Changes

- First version after all pull requests were merged during the libigl hackaton,
and before switching from submodules to CMake external projects.

## Version 1.3.1 Changes

- Last version before pull requests were merged during the libigl hackaton.
- `igl::components` has been renamed to `igl::vertex_components`.
- `viewer.core.model` matrix is gone (#700).

## Version 1.3.0 Changes
List of changes related to this version:

- The CMake build system has been rewritten to be more modular and modern.
  libigl modules are now available as CMake target, e.g. `igl::triangle` or
  `igl::opengl`. See the libigl-example-project for an example of typical
  usage.

- `igl/antweakbar` and `igl/opengl2` support has been removed from the CMake.
  The files are still available, but their use is discouraged.

- The viewer has been refactored and now supports multiple meshes. See related
  tutorial entry for more information. The viewer files are now split
  according to their dependencies. E.g. `igl::viewer::Viewer` has been renamed
  `igl::opengl::glfw::Viewer`.

- NanoGui has been replaced by ImGui, and is now available as a viewer plugin
  instead of `#define`

- Polyvector code has been moved to
  [libdirectional](https://github.com/avaxman/libdirectional) (#630).


## Version 1.2 Changes
This change introduces better organization of dependencies and removes some
deprecated/repeated functions. The 3x3 svd code and dependent functions
(including ARAP) were absorbed into the main library. Similarly, the boost
dependency extra was absorbed.


### External libraries as git subrepos
The core functionality of libigl (still) just depends on stl, c++11 and Eigen.
There are additional _optional_ dependencies (e.g. CGAL, embree, glfw, tetgen,
triangle). Libigl functions using these are located (still) in sub-folders of
the include directory (e.g.  `include/igl/cgal/`, `include/igl/embree/`). Prior
to version 1.2 we included copies of the code for some of these dependencies in the
`external/` directory. As of
version 1.2, these have been replaced with git sub-repos. If you have cloned
libigl _before version 1.2_ then you should issue 

    git submodule update --init --recursive

### Deprecated/repeated functions

Old                                     | New
--------------------------------------- | -----------------------------------
`igl::angles`                           | `igl::internal_angles`
`igl::get_modifiers`                    | [deleted]
`igl::nchoosek(offset,K,N,std::vector)` | `igl::nchoosek(Eigen,K,Eigen)`
`#include <igl/boost/components.h>`     | `#include <igl/components.h>`
`#include <igl/boost/bfs_orient.h>`     | `#include <igl/bfs_orient.h>`
`#include <igl/boost/orientable_patches.h>` | `#include <igl/orientable_patches.h>`
`#include <igl/svd3x3/arap.h>`          | `#include <igl/arap.h>`
`#include <igl/svd3x3/arap_dof.h>`      | `#include <igl/arap_dof.h>`
`#include <igl/svd3x3/fit_rotations.h>` | `#include <igl/fit_rotations.h>`
`#include <igl/svd3x3/polar_svd3x3.h>`  | `#include <igl/polar_svd3x3.h>`
`#include <igl/svd3x3/svd3x3.h>`        | `#include <igl/svd3x3.h>`
`#include <igl/svd3x3/svd3x3_avx.h>`    | `#include <igl/svd3x3_avx.h>`
`#include <igl/svd3x3/svd3x3_sse.h>`    | `#include <igl/svd3x3_sse.h>`


## Version 1.0 Changes
Our beta release marks our confidence that this library can be used outside of
casual experimenting. To maintain order, we have made a few changes which
current users should read and adapt their code accordingly.

### Renamed functions
The following table lists functions which have changed name as of version
1.0.0:

Old                              | New
-------------------------------- | -------------------------------------
`igl::add_barycenter`            | `igl::false_barycentric_subdivision`
`igl::areamatrix`                | `igl::vector_area_matrix`
`igl::barycentric2global`        | `igl::barycentric_to_global`
`igl::boundary_faces`            | `igl::boundary_facets`
`igl::boundary_vertices_sorted`  | `igl::boundary_loop`
`igl::cotangent`                 | `igl::cotmatrix_entries`
`igl::edgetopology`              | `igl::edge_topology`
`igl::gradMat`                   | `igl::grad`
`igl::is_manifold`               | `igl::is_edge_manifold`
`igl::mexStream`                 | `igl::MexStream`
`igl::moveFV`                    | `igl::average_onto_vertices`
`igl::moveVF`                    | `igl::average_onto_faces`
`igl::plot_vector`               | `igl::print_vector`
`igl::pos`                       | `igl::HalfEdgeIterator`
`igl::plane_project`             | `igl::project_isometrically_to_plane`
`igl::project_points_mesh`       | `igl::line_mesh_intersection`
`igl::read`                      | `igl::read_triangle_mesh`
`igl::removeDuplicates.cpp`      | `igl::remove_duplicates`
`igl::removeUnreferenced`        | `igl::remove_unreferenced`
`igl::tt`                        | `igl::triangle_triangle_adjacency`
`igl::vf`                        | `igl::vertex_triangle_adjacency`
`igl::write`                     | `igl::write_triangle_mesh`
`igl::manifold_patches`          | `igl::orientable_patches`
`igl::selfintersect`             | `igl::remesh_self_intersections`
`igl::project_mesh`              | `igl::line_mesh_intersection`
`igl::triangulate`               | `igl::polygon_mesh_to_triangle_mesh`
`igl::is_manifold`               | `igl::is_edge_manifold`
`igl::triangle_wrapper`          | `igl::triangulate`

### Miscellaneous
 - To match interfaces provided by (all) other quadratic optimization
   libraries, `igl::min_quad_with_fixed` and `igl::active_set` now expect as
   input twice the quadratic coefficients matrix, i.e. the Hessian. For
   example, `igl::min_quad_with_fixed(H,B,...)` minimizes $\frac{1}{2}x^T H
   x+x^T B$.
 - We have inverted the `IGL_HEADER_ONLY` macro to `IGL_STATIC_LIBRARY`. To
   compile using libigl as a header-only library, simply include headers and
   libigl in the header search path. To link to libigl, you must define the
   `IGL_STATIC_LIBRARY` macro at compile time and link to the `libigl*.a`
   libraries.
 - Building libigl as a static library is now more organized. There is a
   `build/` directory with Makefiles for the main library (`Makefile`) and each
   dependency (e.g. `Makefile_mosek` for `libiglmosek.a`)
 - `igl::polar_svd` now always returns a rotation in `R`, never a reflection.
   This mirrors the behavior of `igl::polar_svd3x3`.  Consequently the `T`
   part may have negative skews.
 - We have organized the static library build
 - The previous `igl::grad` function, which computed the per-triangle gradient
   of a per-vertex scalar function has been replaced. Now `igl::grad` computes
   the linear operator (previous computed using `igl::gradMat`). The gradient
   values can still be recovered by multiplying the operator against the scalar
   field as a vector and reshaping to have gradients per row.
 - `MASSMATRIX_*` has become `MASSMATRIX_TYPE_*`
 - The function `igl::project_normals`, which cast a line for each vertex of
   mesh _A_ in the normal direction and found the closest intersection along
   these lines with mesh _B_, has been removed.
