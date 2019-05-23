# FAQ

??? faq "I'd like to merge two 3D meshes into one. How to do it with igl?"
    It sounds like you're trying to compute a union. Are your two meshes closed, watertight manifolds? Then you could call `igl/boolean/mesh_boolean` with the union option. If not, then there's still hope with something else. _[Alec]_

??? faq "In other apps I have seen the the user is asked to specify singularities , and the then the rosy field is generated. But in libigl it seems like you have to specify faces and direction vectors to design a field. Is it possible to specify singularities?"
    It is not possible to specify singularities right now. To specify the directions, the vectors should be in global coordinates (the vectors are 3D vectors, the libigl function takes care of projecting them onto the corresponding face), you can take a look here for a basic example that fixes only one face: [Example 505](https://libigl.github.io/tutorial/#global-seamless-integer-grid-parametrization) _[Daniele]_

??? faq "Does Libigl use the same 2D Triangle code (my search in the Libigl source code indicates NO, but a confirmation would be reassuring)?"
    No, it uses CGAL for triangulation. _[Alec]_

??? faq "Libigl's Boolean depends on some GPL-licensed header files from CGAL. Is it possible to remove this dependency?"
    No, the dependency on CGAL would require severely rewriting a core function. It is possible to do, but I will not do it. _[Alec]_

??? faq "Do you have a ready to run command line program so that I can run a test with a few of my sample data sets?"
    No, but it would be very easy to alter the [boolean tutorial example](https://libigl.github.io/tutorial/#boolean-operations-on-meshes) to do that. Basically drop the viewer and change the hardcoded paths to command line arguments and write out the result to an obj. _[Alec]_

??? faq "I see that it can generate N-rosy fields, but is it possible to remesh based on the rosy field?"
    Here is an example that uses libigl to produce a seamless parametrization:
    [Example 505](https://libigl.github.io/tutorial/#global-seamless-integer-grid-parametrization)

    If you want a mesh, you can pass this parametrization to libQEX ([https://github.com/hcebke/libQEx](https://github.com/hcebke/libQEx)) to extract it. We do not have it built in in the tutorial due to a more restrictive licence used by libQEx. _[Daniele]_

??? faq "I am having issues with parameterization (igl::miq). Even at 100 iterations, there are still distortions. What is the cause?"
    This is unfortunately the expected behaviour, the MIQ parametrization tends to concentrate the distortion around singularities. _[Daniele]_

??? faq "I am receiving compilation errors along the lines of "ISO C++ forbids declaration of ... with no type" when compiling under Windows using gcc."
    We never tried to compile libigl on Windows with gcc, but we did test our library on:

    * windows using visual studio
    * linux with gcc
    * macosx with clang

    You might have a version of gcc that doesn't support (enough of) c++11. Try using Cygwin and g++ 4.9.2. _[Alec, Daniele]_

??? faq "What's the deal with CGAL and GCC 4.8?"
    It has come to our attention that CGAL does not work properly with GCC 4.8.
    Please read see #650, and in particular [this thread](http://cgal-discuss.949826.n4.nabble.com/Bugs-in-AABBTree-td4660077.html), for more detailed information. _[Jérémie]_

??? faq "Why do a get a compilation error when writing `contexpr a = 1.0 / 2.0;`?"
    You are likely facing this issue because you are using CGAL 4.12+ with gcc. Starting from 4.12, CGAL now properly supports CMake. In particular, it will propagates flags such as `-frounding-math`, which will cause gcc to produce a compilation error on the code above.
    You can read more about [this issue](https://github.com/CGAL/cgal/issues/3180) in the CGAL bug tracker, and how it may impact your code.
    Our current recommendation is to keep the CGAL parts self-contained as much as possible, and avoid such constructs in the parts of the code that use CGAL. _[Jérémie]_

??? faq "Should I use `Eigen::MatrixBase` or `Eigen::PlainObjectBase` as an argument for my templated functions?"
    - Use `Eigen::MatrixBase` for **inputs** (so you can pass plain matrices, maps and matrix expressions);
    - Use `Eigen::PlainObjectBase` for **outputs** (so the memory can be allocated by the libigl function).

??? faq "I get an `error: Server does not allow request for unadvertised object` when cloning a repository using libigl as a submodule."
    You are probably getting this error because the *libigl history rewriting* that happened on XXX. Read more about this breaking change [here].

??? faq "I have some old GUI code that uses NanoGUI. How can I update it to the latest version of libigl?"
    In 2017, libigl switched from NanoGUI to ImGui for its viewer's user interface. The main reason was to remove nested dependencies in common with libigl, thus providing an overall lighter experience. ImGui also has other advantages, such as more dynamic menus (where you can add/remove elements on the fly), inject UI debugging code in user-code (with [`ImGuiOnceUponAFrame`](https://github.com/ocornut/imgui/blob/a1f3949d7174e4500308a6211c9781f85900bb16/imgui.h#L1187)), etc.

    Porting UI code to ImGui should be relatively straightforward. Have a look at [tutorial 106]({{ repo_url }}/tutorial/106_ViewerMenu/main.cpp), or read issue #719 for more discussion.
    If you would like to keep NanoGUI as your interface library for whatever reason, you are welcome to write a [ViewerPlugin]({{ repo_url }}/include/igl/opengl/glfw/ViewerPlugin.h) reusing the old binding code, and we would be happy to advertise it somewhere.

??? faq "How to write custom shader code in the viewer?"
    See #657.

??? faq "How to draw text in the viewer?"
    See #876.

??? faq "Issues with multi-threading and cgal::CSGTree"
    There is a known race condition that can occur in rare occasions when doing CSG operations with duplicated nodes in the CSG tree, e.g.,
    ```cpp
    igl::copyleft::cgal::CSGTree inter(tree, tree, "i");
    ```
    See an detailed explanation of the problem [here](https://github.com/libigl/libigl/pull/996#issuecomment-450543678), and please use [this thread](https://github.com/libigl/libigl/issues/1086) to discuss the bug if it affects you. So far the problem has only been observed on macOS.
