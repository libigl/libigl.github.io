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

  // Symbol of the page we are on, or null.
  function currentSymbol(path, lang) {
    if (lang === "cpp") {
      // Doxygen file-reference pages: <name>_8h.html, underscores doubled.
      var m = path.match(/\/([^\/]+)_8h\.html$/);
      if (m) return m[1].replace(/__/g, "_").toLowerCase();
      return null;
    }
    if (lang === "py") {
      var h = (location.hash || "").replace(/^#/, "");
      return h ? h.toLowerCase() : null;
    }
    return null;
  }

  function currentLang(path) {
    if (path.indexOf("/dox/") !== -1) return "cpp";
    if (path.indexOf("/python/") !== -1) return "py";
    return "cpp"; // the rest of the main site is the C++ side
  }

  function build(map) {
    var path = location.pathname;
    var lang = currentLang(path);
    var sym = currentSymbol(path, lang);
    var entry = (sym && map[sym]) || {};

    var here = location.pathname + location.hash;
    var cppHref = lang === "cpp" ? here : (entry.cpp || CPP_HOME);
    var pyHref = lang === "py" ? here : (entry.py || PY_HOME);

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
