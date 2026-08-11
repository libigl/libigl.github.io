# Python Bindings

[libigl](https://libigl.github.io) ships NumPy-native Python bindings, published
to PyPI as [`libigl`](https://pypi.org/project/libigl/). Meshes are plain arrays
— `V` an `#V by 3` float array of vertex positions, `F` an `#F by 3` integer
array of faces — and every function returns NumPy arrays or SciPy sparse
matrices.

```bash
python -m pip install libigl
```

```python
import igl
import numpy as np

V, F = igl.read_triangle_mesh("bunny.obj")
L = igl.cotmatrix(V, F)             # sparse cotangent Laplacian
N = igl.per_vertex_normals(V, F)    # per-vertex normals
K = igl.gaussian_curvature(V, F)    # discrete Gaussian curvature
```

## API Reference

The **[Python API Reference](python/api/index.md)** documents every bound
function and class, grouped by module. It is generated directly from the
compiled package, so it always matches the installed bindings. Functions that
also exist in C++ link straight to their [Doxygen reference](dox/index.html)
page, so you can move between the Python and C++ documentation for the same
routine.

## Modules

Core functionality lives in `igl`. Functionality that depends on third-party
libraries is grouped into submodules:

| Module | Contents |
| --- | --- |
| `igl` | core geometry processing (Laplacians, curvature, distances, parametrization, deformation, …) |
| `igl.predicates` | exact geometric predicates (orientation, incircle, winding numbers) |
| `igl.cycodebase` | cubic Bézier / spline distance and root-finding |
| `igl.copyleft`, `igl.copyleft.cgal`, `igl.copyleft.tetgen` | GPL-licensed functionality (booleans, meshing) |
| `igl.embree` | Embree-accelerated ray casting and ambient occlusion |
| `igl.triangle` | Triangle-based 2D meshing |
| `igl.spectra` | Spectra-based sparse eigensolves |

The bindings are developed at
[libigl/libigl-python-bindings](https://github.com/libigl/libigl-python-bindings);
please report missing functions or issues there.
