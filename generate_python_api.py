# NOTE: This is a copy of website/generate_api.py from
# https://github.com/libigl/libigl-python-bindings — keep in sync with it.
"""Generate the Python API reference from the nanobind ``.pyi`` type stubs.

The stubs (emitted by ``nanobind_add_stub`` during the build) are the reliable
source of truth for compiled-module signatures: statically parsing them avoids
importing the extension and sidesteps the introspection quirks of compiled
modules. For every module we emit one Material-for-MkDocs page, and every
function that has a matching ``igl/<name>.h`` header is cross-linked to its C++
Doxygen page on libigl.github.io/dox so the Python and C++ references stay
coherent.

Usage:
    python website/generate_api.py \
        --package igl \
        --igl-include <path-to>/libigl/include \
        --out website/docs/api
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
from collections import Counter
from pathlib import Path


def slugify(name: str) -> str:
    """Match python-markdown's default heading anchor slug for a symbol name."""
    return re.sub(r"[^a-z0-9_]+", "-", name.lower()).strip("-")

DOX_BASE = "https://libigl.github.io/dox"

# Human-facing titles for each module (path -> title). Anything not listed
# falls back to the dotted module name.
MODULE_TITLES = {
    "igl": "igl (core)",
    "igl.copyleft": "igl.copyleft",
    "igl.copyleft.cgal": "igl.copyleft.cgal",
    "igl.copyleft.tetgen": "igl.copyleft.tetgen",
    "igl.cycodebase": "igl.cycodebase",
    "igl.embree": "igl.embree",
    "igl.predicates": "igl.predicates",
    "igl.spectra": "igl.spectra",
    "igl.triangle": "igl.triangle",
}


def clean_annotation(node: ast.AST) -> str:
    """Turn a stub type annotation AST into a compact, readable string.

    nanobind array parameters are annotated as
    ``Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), ...)]``;
    we render those as e.g. ``float64[m, n]``.
    """
    if node is None:
        return ""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{clean_annotation(node.value)}.{node.attr}"
    if isinstance(node, ast.Constant):
        return "None" if node.value is None else repr(node.value)
    if isinstance(node, ast.Tuple):
        return ", ".join(clean_annotation(e) for e in node.elts)
    if isinstance(node, ast.Subscript):
        base = clean_annotation(node.value)
        if base == "Annotated":
            return _clean_annotated(node.slice)
        return f"{base}[{clean_annotation(node.slice)}]"
    # Fallback: best-effort unparse.
    try:
        return ast.unparse(node)
    except Exception:
        return "Any"


def _clean_annotated(slice_node: ast.AST) -> str:
    """Render the payload of an ``Annotated[Base, dict(...)]`` array type."""
    elts = slice_node.elts if isinstance(slice_node, ast.Tuple) else [slice_node]
    dtype = None
    dims = None
    for elt in elts:
        if isinstance(elt, ast.Call):  # the dict(...) metadata
            for kw in elt.keywords:
                if kw.arg == "dtype" and isinstance(kw.value, ast.Constant):
                    dtype = kw.value.value
                elif kw.arg == "shape":
                    letters = ["m", "n", "p", "q"]
                    # A 1-D shape is emitted as `shape=(None)` (a bare value),
                    # a 2-D+ shape as a real tuple `shape=(None, None)`.
                    shape_elts = (kw.value.elts if isinstance(kw.value, ast.Tuple)
                                  else [kw.value])
                    dims = ", ".join(
                        letters[i] if isinstance(d, ast.Constant) and d.value is None
                        else clean_annotation(d)
                        for i, d in enumerate(shape_elts))
    if dtype and dims is not None:
        return f"{dtype}[{dims}]"
    if dtype:
        return f"{dtype}[...]"
    return "ArrayLike"


def render_signature(fn: ast.FunctionDef) -> str:
    """Render a def's argument list, dropping ``self`` and cleaning types."""
    a = fn.args
    parts = []
    defaults = [None] * (len(a.args) - len(a.defaults)) + list(a.defaults)
    for arg, default in zip(a.args, defaults):
        if arg.arg == "self":
            continue
        s = arg.arg
        if arg.annotation is not None:
            s += f": {clean_annotation(arg.annotation)}"
        if default is not None:
            s += f" = {clean_annotation(default)}"
        parts.append(s)
    ret = f" -> {clean_annotation(fn.returns)}" if fn.returns else ""
    return f"{fn.name}({', '.join(parts)}){ret}"


def _esc(text: str) -> str:
    """Escape a leading '#' so libigl's '#V'/'#E'/'#F' ("number of") notation
    isn't parsed as a Markdown heading (python-markdown accepts space-less
    '#heading'), which would otherwise pollute the table of contents."""
    return re.sub(r"^(\s*)(#+)", r"\1\\\2", text)


def format_docstring(doc: str) -> str:
    """Turn a doxygen-style docstring into Material markdown.

    The leading prose becomes the description; ``@param[in|out] name  text``
    lines become a Parameters list and ``@return`` becomes Returns.
    """
    if not doc:
        return "_No description available._\n"
    lines = [l.rstrip() for l in doc.strip("\n").splitlines()]
    desc, params, returns = [], [], []
    bucket = desc
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("@param"):
            rest = stripped.split(None, 1)[1] if " " in stripped else ""
            params.append(rest)
            bucket = params
        elif stripped.startswith(("@return", "@returns")):
            rest = stripped.split(None, 1)[1] if " " in stripped else ""
            returns.append(rest)
            bucket = returns
        elif stripped.startswith("\\see") or stripped.startswith("@see"):
            bucket = None  # drop see-also cross-refs for now
        elif bucket is not None:
            if bucket is desc:
                bucket.append(line)
            elif stripped:  # continuation of a param/return entry
                bucket[-1] += " " + stripped

    out = []
    text = "\n".join(_esc(l) for l in desc).strip()
    if text:
        out.append(text + "\n")
    if params:
        out.append("**Parameters**\n")
        for p in params:
            name, _, rest = p.partition(" ")
            out.append(f"- `{name}` — {_esc(rest.strip())}")
        out.append("")
    if returns:
        out.append("**Returns**\n")
        for r in returns:
            out.append(f"- {_esc(r.strip())}")
        out.append("")
    return "\n".join(out) + "\n"


def module_for(stub: Path, package_parent: Path) -> str:
    """Dotted module name from a stub path (its parent dir under the package)."""
    rel = stub.parent.relative_to(package_parent)
    return ".".join(rel.parts)


def _split_top_level(argstr: str):
    """Split a signature argument list on top-level commas (bracket-aware)."""
    parts, depth, cur = [], 0, ""
    for ch in argstr:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def _repair_arg_order(src: str) -> str:
    """Give every argument a default once any earlier one has one.

    nanobind occasionally emits a required argument after an optional one
    (e.g. mesh_boolean's ``type_str``), which is not valid Python. Adding a
    synthetic ``= ...`` makes the stub parseable; such args render with ``...``.
    """
    open_i = src.find("(")
    if open_i < 0:
        return src
    depth, close_i = 0, -1
    for i in range(open_i, len(src)):
        if src[i] in "([{":
            depth += 1
        elif src[i] in ")]}":
            depth -= 1
            if depth == 0:
                close_i = i
                break
    if close_i < 0:
        return src
    args = _split_top_level(src[open_i + 1:close_i])
    seen_default = False
    fixed = []
    for i, a in enumerate(args):
        # Name any unnamed parameter (nanobind sometimes drops the name, e.g.
        # "(: Annotated[...]" when a binding omits the argument label).
        if a.lstrip().startswith(":"):
            lead = a[:len(a) - len(a.lstrip())]
            a = f"{lead}arg{i}{a.lstrip()}"
        has_default = "=" in _strip_brackets(a)
        if seen_default and not has_default and a.strip():
            a = a + " = ..."
            has_default = True
        seen_default = seen_default or has_default
        fixed.append(a)
    return src[:open_i + 1] + ",".join(fixed) + src[close_i:]


def _strip_brackets(s: str) -> str:
    """Remove bracketed spans so a top-level '=' can be detected."""
    out, depth = "", 0
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif depth == 0:
            out += ch
    return out


def _parse_tolerant(text: str):
    """Parse a stub, repairing the invalid signatures nanobind sometimes emits.

    Each stub signature is a single line, so we repair argument ordering on
    every ``def`` line (see _repair_arg_order) before parsing the whole file,
    which keeps ``@overload`` decorators attached to their functions.
    """
    try:
        return ast.parse(text).body
    except SyntaxError:
        pass
    repaired = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("def ") and line.rstrip().endswith(":"):
            repaired.append(_repair_arg_order(line))
        else:
            repaired.append(line)
    try:
        return ast.parse("".join(repaired)).body
    except SyntaxError as e:
        print(f"  warning: stub still unparseable after repair: {e}")
        return []


def collect(stub: Path):
    """Return (functions, classes) from a stub, merging @overload groups."""
    functions, classes = {}, []
    for node in _parse_tolerant(stub.read_text()):
        if isinstance(node, ast.FunctionDef):
            functions.setdefault(node.name, []).append(node)
        elif isinstance(node, ast.ClassDef):
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)
                       and not n.name.startswith("__")]
            classes.append((node, methods, ast.get_docstring(node)))
    return functions, classes


def dox_filename(name: str) -> str:
    """Doxygen file-reference page filename for igl/<name>.h.

    Doxygen mangles the output name by turning '.h' into '_8h' and doubling
    every underscore; case is preserved (e.g. marching_cubes.h ->
    marching__cubes_8h.html, AABB.h -> AABB_8h.html)."""
    return f"{name.replace('_', '__')}_8h.html"


def resolve_cpp(name, subpath, dox_pages):
    """Resolve a symbol to its Doxygen page filename, honoring collisions.

    Doxygen keeps a unique filename plain (e.g. mesh_boolean.h ->
    mesh__boolean_8h.html even under copyleft/cgal/) but disambiguates a
    duplicate by prefixing its directory, encoding '/' as '_2' (e.g.
    igl/copyleft/marching_cubes.h -> copyleft_2marching__cubes_8h.html while the
    core igl/marching_cubes.h stays marching__cubes_8h.html). We try the
    most-specific prefixed candidate down to the plain one and pick the first
    that actually exists in the Doxygen page list."""
    cands = []
    for i in range(len(subpath) + 1):
        prefix = "".join(seg.replace("_", "__") + "_2" for seg in subpath[i:])
        cands.append(prefix + dox_filename(name))
    if dox_pages is None:
        return cands[-1]  # best-effort plain name when unvalidated
    for c in cands:
        if c in dox_pages:
            return c
    return None


def cpp_chip(cpp_page) -> str:
    """A standalone C++ cross-link line placed under a heading (kept out of the
    heading so it does not leak into the table of contents)."""
    if cpp_page:
        return f"[:material-language-cpp: C++ reference]({DOX_BASE}/{cpp_page}){{ .cpp-xref }}\n"
    return ""


def emit_function(name, defs, cpp_page) -> str:
    out = [f"### {name}\n"]
    chip = cpp_chip(cpp_page)
    if chip:
        out.append(chip)
    seen = set()
    for fn in defs:
        sig = render_signature(fn)
        out.append(f"```python\n{sig}\n```\n")
        doc = ast.get_docstring(fn)
        if doc and doc not in seen:
            seen.add(doc)
            out.append(format_docstring(doc))
    return "\n".join(out)


def emit_class(node, methods, doc, cpp_page) -> str:
    out = [f"### {node.name}\n"]
    chip = cpp_chip(cpp_page)
    if chip:
        out.append(chip)
    if doc:
        out.append(format_docstring(doc))
    for m in methods:
        out.append(f"#### {node.name}.{m.name}\n")
        out.append(f"```python\n{render_signature(m)}\n```\n")
        mdoc = ast.get_docstring(m)
        if mdoc:
            out.append(format_docstring(mdoc))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", default="igl", help="path to the igl package dir")
    ap.add_argument("--igl-include", default="", help="path to libigl include/ dir")
    ap.add_argument("--dox-index", default="",
                    help="Doxygen files.html (or any page listing) for the "
                         "target /dox/ site; links are validated against it so "
                         "none 404. Omit to link by header-name heuristic only.")
    ap.add_argument("--out", default="website/docs/api")
    ap.add_argument("--url-base", default="/python/api",
                    help="site-root URL under which the API pages are served; "
                         "used to build the symbol_map.json toggle links")
    args = ap.parse_args()

    package = Path(args.package).resolve()
    package_parent = package.parent
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # The set of Doxygen pages that actually exist, from the target /dox/ page
    # list. Cross-links (and the toggle) are resolved against this so they never
    # 404 and so collisions map to the right disambiguated page.
    dox_pages = None
    if args.dox_index:
        dox_pages = set(re.findall(r"[A-Za-z0-9_]+_8h\.html",
                                   Path(args.dox_index).read_text()))

    stubs = sorted(package.rglob("pyigl_*.pyi"))
    index_rows = []
    # Two lookup tables for the toggle: Python anchor -> C++ page, and C++ page
    # filename -> Python anchor URL (so both directions resolve exactly, even
    # for directory-disambiguated pages like copyleft_2marching__cubes_8h.html).
    symbol_map = {"sym2cpp": {}, "cpp2py": {}}

    def record(name, stem, cpp_page):
        slug = slugify(name)
        py_url = f"{args.url_base}/{stem}/#{slug}"
        if cpp_page:
            symbol_map["sym2cpp"][slug] = f"/dox/{cpp_page}"
            symbol_map["cpp2py"][cpp_page] = py_url

    for stub in stubs:
        module = module_for(stub, package_parent)
        title = MODULE_TITLES.get(module, module)
        functions, classes = collect(stub)
        stem = module.replace(".", "_")
        subpath = module.split(".")[1:]  # e.g. ["copyleft", "cgal"]
        page = [f"# {title}\n"]
        page.append(f"Python API reference for `{module}`.\n")
        for name in sorted(functions):
            cpp = resolve_cpp(name, subpath, dox_pages)
            page.append(emit_function(name, functions[name], cpp))
            record(name, stem, cpp)
        for node, methods, doc in sorted(classes, key=lambda c: c[0].name):
            cpp = resolve_cpp(node.name, subpath, dox_pages)
            page.append(emit_class(node, methods, doc, cpp))
            record(node.name, stem, cpp)
        fname = stem + ".md"
        (out / fname).write_text("\n".join(page))
        n = len(functions) + len(classes)
        index_rows.append((title, fname, n))
        print(f"  {module}: {len(functions)} functions, {len(classes)} classes -> {fname}")

    (out / "symbol_map.json").write_text(json.dumps(symbol_map, sort_keys=True))
    print(f"  wrote symbol_map.json "
          f"({len(symbol_map['sym2cpp'])} symbols cross-linked)")

    # An index page listing every module.
    idx = ["# API Reference\n",
           "Auto-generated from the compiled bindings' type stubs. Functions with "
           "a C++ counterpart link to the [C++ Doxygen reference]"
           f"({DOX_BASE}/).\n",
           "| Module | Symbols |", "| --- | --- |"]
    for title, fname, n in index_rows:
        idx.append(f"| [{title}]({fname}) | {n} |")
    (out / "index.md").write_text("\n".join(idx) + "\n")
    print(f"Wrote {len(stubs)} module pages + index to {out}")


if __name__ == "__main__":
    main()
