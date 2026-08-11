/*
 * Persistent C++ / Python language toggle shared by the MkDocs pages and the
 * Doxygen (/dox/) pages of the libigl site.
 *
 * Behaviour: toggling jumps to the *equivalent* page in the other language when
 * one exists (per symbol), otherwise falls back to that language's reference
 * home. The mapping is symbol_map.json, generated from the Python bindings.
 */
(function () {
  "use strict";

  var MAP_URL = "/python/api/symbol_map.json";
  var PY_HOME = "/python/api/";
  var CPP_HOME = "/dox/index.html";

  function currentLang(path) {
    if (path.indexOf("/dox/") !== -1) return "cpp";
    if (path.indexOf("/python/") !== -1) return "py";
    return "cpp"; // the rest of the main site is the C++ side
  }

  function build(map) {
    var sym2cpp = map.sym2cpp || {};
    var cpp2py = map.cpp2py || {};
    var path = location.pathname;
    var lang = currentLang(path);
    var here = path + location.hash;

    var cppHref, pyHref;
    if (lang === "py") {
      pyHref = here;
      var sym = (location.hash || "").replace(/^#/, "").toLowerCase();
      cppHref = (sym && sym2cpp[sym]) || CPP_HOME;
    } else {
      cppHref = here;
      // Look up this Doxygen page's filename directly (handles the
      // directory-disambiguated names like copyleft_2marching__cubes_8h.html).
      var fname = path.split("/").pop();
      pyHref = cpp2py[fname] || PY_HOME;
    }

    var el = document.createElement("div");
    el.className = "lang-toggle";
    el.setAttribute("role", "group");
    el.setAttribute("aria-label", "Documentation language");
    el.innerHTML =
      '<a data-lang="cpp"' + (lang === "cpp" ? ' class="lang-toggle__active"' : "") +
        ' href="' + cppHref + '">C++</a>' +
      '<a data-lang="py"' + (lang === "py" ? ' class="lang-toggle__active"' : "") +
        ' href="' + pyHref + '">Python</a>';

    // Prefer to sit inside the Material header; otherwise float (Doxygen).
    var header = document.querySelector(".md-header__inner");
    if (header) {
      var source = header.querySelector(".md-header__source");
      header.insertBefore(el, source || null);
    } else {
      el.className += " lang-toggle--fixed";
      document.body.appendChild(el);
    }
  }

  function init() {
    fetch(MAP_URL)
      .then(function (r) { return r.ok ? r.json() : {}; })
      .catch(function () { return {}; })
      .then(build);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
