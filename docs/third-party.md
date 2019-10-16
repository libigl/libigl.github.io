The `external/` directory contains external libraries which are either difficult to obtain, difficult to compile or patched for libigl.

## Embree

Install `ispc`  and `tbb` for example (`brew install ispc tbb`), then

```bash
mkdir build
cd build
cmake -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_BUILD_TYPE=Release ..
make
```

## TinyXML2

double precision bug fixes:

tinyxml2.h line 1286 add function:

```cpp
void SetAttribute( const char* name, float value ) {
	XMLAttribute* a = FindOrCreateAttribute( name );
	a->SetAttribute( value );
}
```

tinyxml2.cpp line 434 replace with:

```cpp
TIXML_SNPRINTF( buffer, bufferSize, "%.15e", v );
```

## CGAL

CGAL can be built as a CMake external project thanks to the `CMakeLists.txt` provided in this folder. While this is mainly intended as a convenience for Windows users, and CI builds on AppVeyor, this should work on Linux/macOS as well. To build CGAL and Boost with the provided CMake script, build this folder as you would compile any CMake project (use CMake GUI and MSVC on Windows):

```bash
mkdir build
cd build
cmake ..
make -j4
```

Once this is done, just build the libigl tutorials, and it should properly detect CGAL and Boost.


## bbw
This library extra contains functions for computing Bounded Biharmonic Weights, can be used with and without the [mosek](#mosek) extra via the `IGL_NO_MOSEK` macro.

## boolean
This library extra contains functions for computing mesh-mesh booleans,
depending on CGAL and optionally Cork.

## embree
This library extra utilizes embree's efficient ray tracing queries.

## matlab
This library extra provides support for reading and writing `.mat` workspace
files, interfacing with Matlab at run time and compiling mex functions.

## mosek
This library extra utilizes mosek's efficient interior-point solver for
quadratic programs.

## png
This library extra uses `libpng` and `YImage` to read and write `.png` files.

## tetgen
This library extra provides a simplified wrapper to the tetgen 3d tetrahedral
meshing library.

## Triangle
This library extra provides a simplified wrapper to the triangle 2d triangle
meshing library.

## xml
This library extra utilizes tinyxml2 to read and write serialized classes
containing Eigen matrices and other standard simple data-structures.

## Optional

- OpenGL (disable with `LIBIGL_WITH_OPENGL` set to `OFF`)
    * OpenGL >= 4 (enable with `IGL_OPENGL_4`)
- GLEW  Windows and Linux
- OpenMP
- libpng  libiglpng extra only
- Mosek  libiglmosek extra only
- Matlab  libiglmatlab extra only
- boost  libiglboost, libiglcgal extra only
- SSE/AVX  libiglsvd3x3 extra only
- CGAL  libiglcgal extra only
    * boost
    * gmp
    * mpfr
- CoMiSo libcomiso extra only

## Optional (included in external/)

- TetGen  libigltetgen extra only
- Embree  libiglembree extra only
- tinyxml2  libiglxml extra only
- glfw libviewer extra only
- LIM  liblim extra only
