libigl file formats
===================

- [.bf](./bf) ASCII files for representing skeletal bone "forests"
- [.dmat](./dmat) uncompressed ASCII/binary files for dense matrices
- *.ele* Element (triangle or tet) list. This format comes in similar flavors: [tetgen's](http://tetgen.berlios.de/fformats.ele.html), [stellar's](http://www.cs.berkeley.edu/~jrs/stellar/#fileformats), and [triangle's](https://www.cs.cmu.edu/~quake/triangle.ele.html). The formats of TetGen and stellar are identical upto conventions on index ordering and number of allowed attributes (unverified).
- [.face](http://wias-berlin.de/software/tetgen/fformats.face.html) TetGen's file format for simplicial facets.
- [.mesh](https://www.ljll.math.upmc.fr/frey/publications/RT-0253.pdf#page=33) Medit's triangle surface mesh + tetrahedral volume mesh file format, see page 33, section 7.2.1
- [.msh](https://gmsh.info/doc/texinfo/gmsh.html#MSH-file-format-version-2-_0028Legacy_0029) Gmsh finite element mesh generator legacy version 2 file format. This format is very flexible and supports mixture of various elements, each vertex and each element can also have arbitrary number of scalar or vector fields defined, also elements are assigned integer tags to define sub meshes. Currently only triangular and tetrahedral elements are supported. Both ASCII and binary encodings are supported.
- *.node* List of points (vertices). Described identically (upto accepted dimensions, use of attributes and boundary markers) by [Triangle](https://www.cs.cmu.edu/~quake/triangle.node.html), [TetGen](http://tetgen.berlios.de/fformats.node.html), and [Stellar](http://www.cs.berkeley.edu/~jrs/stellar/#fileformats).
- [.off](http://wias-berlin.de/software/tetgen/fformats.off.html) Geomview's polyhedral file format
- [.obj](http://en.wikipedia.org/wiki/Wavefront_.obj_file#File_format) Wavefront object file format. Usually unsafe to assume anything more than vertex positions and triangle indices are supported
- [.ply](http://en.wikipedia.org/wiki/PLY_%28file_format%29) Polygon File Format, supporting ASCII and binary encoding. Each vertex and element can have artitrary number of additional properties.
- [.png](https://en.wikipedia.org/wiki/Portable_Network_Graphics) Portable Network Graphics image file. libigl supports png image files via the [stb image](http://nothings.org/stb_image.h) library. Alpha channels and compression are supported.
- *.poly* Piecewise-linear complex. This format comes in many similar but importantly different flavors: [triangle's](https://www.cs.cmu.edu/~quake/triangle.poly.html), [tetgen's](http://tetgen.berlios.de/fformats.poly.html), [pyramid/SVR's](http://sparse-meshing.com/svr/0.2.1/format-poly.html)
- [.rbr](./rbr) ASCII files for saving state of ReAntTweakBar
- [.stl](http://en.wikipedia.org/wiki/STL_(file_format)) 3D Systems'CAD and 3D printing mesh file format. ASCII and binary versions.
- [.tga](http://en.wikipedia.org/wiki/Truevision_TGA) Truevision TGA or TARGA image file format. IGLLIB supports only very basic reading and writing RGB/RGBA files without colormaps and (unverified) run-length compression.
- [.tgf](./tgf) ASCII files for representing control handle graphs
- [.wrl](http://en.wikipedia.org/wiki/VRML#WRL_File_Format) VRML (Virtual Reality Modeling Language) file format for 3D scenes.
- [.xml](./xml) XMLSerializer's file format containing the serialization of object data structures.


### Triangle mesh file format performance

[.obj](http://en.wikipedia.org/wiki/Wavefront_.obj_file#File_format) and [.off](http://tetgen.berlios.de/fformats.off.html) file formats support meshes with arbitrary polygon degrees. However, often we are only working with triangle meshes. Further, .obj files do not have useful headers revealing the number of elements. For triangle meshes, .off and .obj are inferior file formats to the [.mesh](http://www.ann.jussieu.fr/frey/publications/RT-0253.pdf#page=33) file format. The current (version 0.1.6) IO functions for these file formats perform as follows for reading and writing a 300,000 triangle mesh:

    writeOBJ:  1.33742 secs
    writeOFF:  0.510111 secs
    writeMESH: 0.218139 secs

    readOBJ:   1.3782 secs
    readOFF:   0.691496 secs
    readMESH:  0.242315 secs

This reveals that .mesh is 6.5x faster than .obj and about 2.5x faster than .off.

While .obj files support normals, it is typically much faster to (re)compute normals from the geometry using `per_face_normals`, `per_vertex_normals`, `per_corner_normals` than to read and write them to files.

It gets even better if you're willing to use a nonstandard format. If your triangle mesh is in (`V`,`F`) then you can read and write those variables as dense matrices of doubles to [.dmat](./dmat) uncompressed **binary** files. This not only ensures perfect precision but also big speed ups. On that same 300,000 triangle mesh, .dmat achieves:

    writeDMAT: 0.0384338 secs

    readDMAT:  0.0117921 secs

This reveals that binary .dmat files are 34x/116x faster at writing and reading than .obj and a hefty 5x/20x over .mesh. In this case it may pay to compute normals once into `N` and also read and write it to a .dmat file.
