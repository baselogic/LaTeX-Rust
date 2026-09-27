# Changelog

## [1.2.0] — 2026-09-27

### Added

- Expose `render::glyph_render_scale` as the checked renderer boundary for external backends consuming `MathBox` glyphs. The API derives the character and glyph id from the box so callers cannot supply mismatched scale inputs.
- Add a differential LuaLaTeX layout oracle and its stress corpus next to the math engine so it measures `MathBox` directly rather than a downstream repair/display-list layer.
- Add the 158-case accepted-layout corpus as direct parser/layout coverage.

## [1.1.0] — 2026-09-27

### Added

- Added `layout_with_em_size_pt` and `layout_with_numbering_and_em_size_pt` for callers that need correct normalization of absolute TeX dimensions at a known physical math em size.

### Fixed

- Prevent exact-rational decimal formatting from overflowing while processing large remainders.
- Reject egui tessellation vertex and index values that do not fit in `u32` instead of truncating them.
- Use mathematical italic Unicode characters for default bare math variables without overriding explicit text styles.
- Correct fixed and wide hat/tilde variant selection, OpenType MATH attachment, vertical placement, nucleus width, and nested-accent geometry.
- Correct radical variant selection, surd/rule geometry, and radical-degree positioning.
- Restore physical `\nulldelimiterspace` around delimiter-less fractions.
- Apply TeX delimiter factor/shortfall sizing and MATH-axis centering.
- Correct display large-operator axis alignment, limit placement, and branch recentering.
- Restore ordinary-row math italic correction without duplicating scripted-nucleus correction.
- Apply OpenType `ssty` alternates and the correct glyph scale in Script and ScriptScript styles.
- Scale `SpaceAfterScript` in the parent math style.
- Apply the full OpenType MATH vertical constraints for paired subscripts and superscripts.
- Correct AMSMath matrix, cases, aligned, and substack layout geometry.
- Correct display integral `\nolimits` script geometry, including MATH-axis centering, baseline-drop constraints, and italic-correction anchoring.

## [1.0.4] — 2026-09-20

Clippy debt clear (`-D warnings`): `RowKind::Intertext` boxed to shrink enum size.

## [1.0.3] — 2026-09-19

Coordinated patch with zenith-float, hdf5-rust, and redb-view (pure-Rust FOSS family adjacent to Accumath; Accumath itself stays proprietary).

## [1.0.2] — 2026-09-04

Standalone layout math. This crate does not depend on a numeric library.

- `Dim` is an exact rational (`num/den`). No hardware `f32`/`f64` in layout.
- SHA-256 of the embedded face is in-tree.
- Removed the numeric-library dependency from `Cargo.toml`.

## [1.0.0] — 2026-09-02

### Added

- Complete LaTeX math parser (`parse`, gold-stable `MathNode`)
- TeX-faithful layout engine (Appendix G style, Table 18 spacing, `Dim`)
- SVG renderer (`render_svg` / `latex_to_svg`) — self-contained SVG 1.1, no font embedding
- PNG renderer (feature `png`) via `tiny-skia` 0.11, DPI-aware, transparent background by default
- egui renderer (feature `egui`) — TrueType tessellation to `egui::Shape` meshes, no SVG intermediate
- Math-mode symbol catalog (Greek, AMS, arrows, operators, font styles) locked to `data/symbols.tsv`
- Full accent and decoration support (TeX placement, extensible hats/arrows/braces, cancel, boxed)
- Multiline environments — `align`, `aligned`, `split`, `gather`, `multline`, `equation`, `{array}`, `{cases}`
- Color support — named, rgb, RGB, HTML, cmyk, gray, `\definecolor`, group scope, `\fcolorbox` borders
- Exact-rational layout math (no hardware `f32`/`f64` in layout)

### Milestone notes

Milestones 1–10 landed as 0.1.0 development commits. This release packages that
surface as 1.0.0: rustdoc, README benchmarks, clippy/fmt, and crates.io metadata.
The crate is publish-ready; crates.io upload is a separate step.

### [1.0.1] - 2026-09-02

### Version to 1.0.1
### Fixed

Resolved an issue where the docs.rs documentation build was failing due to deprecated Rust nightly features (doc_auto_cfg).
Removed:  two temporary build documents Prompt and color addition
Corrected email address of author from jscarr@gmail.com to jscarr1964@gmail.com

### Architecture

Crate modules: `parser/`, `layout/`, `font/`, `render/svg`, `render/png`,
`render/egui`, plus `golds/` and `benches/` in the repository.
