# Unit Tests for [libigl](https://github.com/libigl/libigl)

The libigl unit test are included in the main repository inside the `tests` folder.
There is a cmake flag to enable/disable the testings `LIBIGL_BUILD_TESTS` which is
disable by default when libigl is not a *toplevel project*, that is you are using
libigl as a library in your own project.


## Dependencies

[Catch2](https://github.com/catchorg/Catch2) is a auto-download dependency.


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

We refer to [Catch2 manual](https://github.com/catchorg/Catch2/tree/master/docs) for additional options.


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

You can use functions like `test_common::assert_eq` to assert equality.
The [cumsum test](https://github.com/libigl/libigl/blob/master/tests/include/igl/cumsum.cpp) is a good
simple example of a test case.

Many libigl functions act on triangle meshes, you can use the utility `test_common::load_mesh("cube.obj", V, F)`
to load some data.

**Note** the data used for testing is not in this repository. Instead it is contained in the [libigl-tests-data](https://github.com/libigl/libigl-tests-data) repo. It is automatically downloaded when `LIBIGL_BUILD_TESTS` is enabled.


## Conventions

When naming a test for a function `igl::extra::function_name` use:

```cpp
TEST_CASE(extra_function_name, "[igl/extra]")
{
  ...
}
```

where `meaning_test_name` could identify the type of test or the type of data
being used.

### Example

The test for `igl::copyleft::cgal::order_facets_around_edges` in
`include/igl/copyleft/cgal/order_facets_around_edges.cpp` is:

```cpp
TEST_CASE("copyleft_cgal_order_facets_around_edges", "[igl/copyleft/cgal]")
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
