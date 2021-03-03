Before opening an issue on creating a pull request, please check the following:

!!! tip
    
    - Make sure you read the
      [**FAQ**](https://github.com/libigl/libigl/wiki/FAQ) before asking a new
      question, search [**existing
      issues**](https://github.com/libigl/libigl/issues?q=is%3Aissue+is%3Aclosed)
      for a problem similar to yours.

    - Make sure you read the information contained in the libigl
      [**homepage**](https://github.com/libigl/libigl) as well as the
      [**tutorial**](https://libigl.github.io/tutorial).

## General Issues

- Make sure you are up-to-date with the **main** branch, and verify that
  your issue has not been fixed already before opening an issue on github.

- To report a problem about the **website** (out-of-date content, erroneous
  instructions or errors in the tutorial), please open your issue in the
  designated [repository](https://github.com/libigl/libigl.github.io/issues)
  for the website.

## Compilation Issues

- If you are on Windows, did you select the **x64** version of the Visual
  Studio compiler?

- If you have a **CMake issue**, make sure you follow the same approach as the
  [libigl-example-project](https://github.com/libigl/libigl-example-project)
  to build libigl with your project, and make sure that you can compile the
  example project. Please also make sure to delete your **CMakeCache.txt**,
  or delete your **build/** folder and try again.

- If you have an issue with a **submodule**, then you are using an old version
  of libigl. Please read [this page](/rewritten-history) about the transition
  to v2.0.0.

- If you have an issue with downloading an **external dependency** using the
  CMake build, delete the `external/` folder and try again.

- If you have an issue with a missing **template**, check that your code
  compiles with the *header-only* option of libigl activated. Turn **`OFF`**
  the CMake option `LIBIGL_USE_STATIC_LIBRARY`: either modify your
  `CMakeCache.txt` via CMake GUI or ccmake, or delete your `CMakeCache.txt`
  and re-run `cmake -DLIBIGL_USE_STATIC_LIBRARY=OFF ..` in your build folder.

- If none of these solve your problem, then please report your issue in the
  bug tracker!
