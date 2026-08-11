"""Inject the shared C++/Python language toggle into generated Doxygen pages.

Doxygen output has no hook for our toggle, so after `doxygen` runs we add a
stylesheet <link> and the toggle <script> to every generated page. Both use
site-root-absolute URLs, served by MkDocs from docs/css and docs/js.

Usage: python inject_dox_toggle.py docs/dox
"""
import sys
from pathlib import Path

HEAD = '<link rel="stylesheet" href="/css/lang-toggle.css">'
BODY = '<script src="/js/lang-toggle.js"></script>'


def main(root):
    n = 0
    for f in Path(root).rglob("*.html"):
        t = f.read_text(errors="ignore")
        if "lang-toggle.js" in t:
            continue
        if "</head>" in t:
            t = t.replace("</head>", HEAD + "\n</head>", 1)
        if "</body>" in t:
            t = t.replace("</body>", BODY + "\n</body>", 1)
        f.write_text(t)
        n += 1
    print(f"injected language toggle into {n} Doxygen pages")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs/dox")
