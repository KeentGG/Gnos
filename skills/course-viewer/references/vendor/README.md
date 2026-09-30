# Viewer assets

These pinned browser files ship with each rendered course page so math and
code work without a CDN request.

- `katex/`: KaTeX 0.16.11 from the `katex` npm package. The minified CSS
  uses its WOFF2 font files. See `katex/LICENSE`.
- `highlight/`: highlight.js 11.11.1 from the `@highlightjs/cdn-assets`
  npm package. The local bundle supports automatic language detection. See
  `highlight/LICENSE`.

`render_viewer.py` copies this directory to `portal/assets/` beside
`index.html`. `serve_course.py` exposes only filenames present here, in
addition to registered ready artifacts.
