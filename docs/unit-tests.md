# Unit Tests for libigl

The libigl unit test are included in the main repository inside the `tests` folder.
There is a CMake flag to enable/disable the testings `LIBIGL_BUILD_TESTS` which is
disabled by default when libigl is not a *toplevel project*, that is when you are using
libigl as a library in your own project.


!!! tip
    Before writing any new unit test, be sure you are using the `dev` branch to use the latest version of libigl available.


## Dependencies

- [Catch2](https://github.com/catchorg/Catch2) is an auto-downloaded dependency.


## Build and test

Use `cmake` to generate a `Makefile` that will build _and test_ upon issuing
`make`:

```
mkdir build
cd build
cmake ..
```

Then build and test with

```
make
make test
```

This will first compile the tests and then immediately run the tests. If tests
are succeeding you should see output similar to:

```
Test project /usr/local/libigl-unit-tests/build
    Start 1: run_igl_mosek_tests
1/4 Test #1: run_igl_mosek_tests ..............***Exception: Other  0.00 sec
    Start 2: run_igl_boolean_tests
2/4 Test #2: run_igl_boolean_tests ............   Passed    1.12 sec
    Start 3: run_igl_cgal_tests
3/4 Test #3: run_igl_cgal_tests ...............   Passed    2.46 sec
    Start 4: run_igl_tests
```

We refer to the [Catch2 manual](https://github.com/catchorg/Catch2/tree/master/docs) for additional options.


## Generating new tests

To create a new test, just create a file with the same name of the file you want to test
inside the `include\igl` in the `tests` folder. Then just add
```cpp
#include <test_common.h>

TEST_CASE("<function_name> <possible description>", "[igl]")
{
  \\test code goes here
}
```

You can use functions like `test_common::assert_eq` to assert equality between two Eigen matrices.
The [cumsum test](https://github.com/libigl/libigl/blob/master/tests/include/igl/cumsum.cpp) is a good
simple example of a test case.

Many libigl functions act on triangle meshes, you can use `igl::read_triangle_mesh(test_common::data_path("cube.obj"), V, F)` to load a triangle mesh located in the test data folder.

!!! note
    The data used for testing is not in the main libigl repository. Instead it is contained in the [libigl-tests-data](https://github.com/libigl/libigl-tests-data) repository. It is automatically downloaded when `LIBIGL_BUILD_TESTS` is enabled.


## Conventions

When naming a test for a function `igl::extra::function_name` use:

```cpp
TEST_CASE("function_name: my_description", "[igl/extra]")
{
  ...
}
```

where `my_description` can be used to identify the type of unit test being run on the function `function_name`.

### Example

The test for `igl::copyleft::cgal::order_facets_around_edges` in
`include/igl/copyleft/cgal/order_facets_around_edges.cpp` is:

```cpp
TEST_CASE("copyleft_cgal_order_facets_around_edges: Simple", "[igl/copyleft/cgal]")
{
  ...
}
```

which tests this function on example data containing a triplet of faces.

## Guarantees

None.

(Obviously?) The presence of a unit test here for some function (e.g.,
`igl::cotmatrix`) is not a guarantee or even an endorsement of the notion that
the libigl function `igl::cotmatrix` is bug free or "fully tested" or "heavily
tested" or even "adequately tested".

## Need work?

Some of the most used libigl functions

```bash
grep -hr "^#include \"" ../libigl/include/igl | sed -e 's/\(\.\.\/\)//g' | sort | uniq -c | sort
```

still don't have unit tests.
