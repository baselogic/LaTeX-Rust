# Historical math-fix provenance migrated from `latex-rust-fixes`

Status: historical migration evidence. This file is not the current semantic contract for
LaTeX-Rust 1.2.0. The compatibility shim described below was retired after its mathematical
repairs were integrated into LaTeX-Rust. Current behavior is owned by the implementation and
regression tests in this repository; the LuaLaTeX differential oracle is documented in
`documents/MATH_ORACLE.md`.

The original identifiers are preserved so prior audit references remain reconstructible. Statements
about `latex-rust-fixes`, its paths, and its dependency on upstream `latex-rust 1.0.2` describe the
pre-1.2.0 architecture and must not be read as current instructions.

## Current ownership map

| Historical provenance | Current primary evidence |
| --- | --- |
| `P-LATEX-WIDE-ACCENT-001` | `tests/wide_accent_math.rs` |
| `P-LATEX-RADICAL-JOIN-001`, `P-LATEX-RADICAL-DEGREE-001` | `tests/radical_geometry.rs`, `tests/radical_variant.rs` |
| `C-LATEX-RUST-COMPAT-AUDIT-001` | Superseded by the integrated 1.2.0 implementation and release commit `5c35f3d3fbd781dd1d9bd392a1b4b7bfa4229b69` |
| `P-LATEX-FRACTION-NULL-DELIM-001` | `tests/fraction_null_delimiter.rs` |
| `P-LATEX-LARGE-OP-LIMITS-001`, `P-LATEX-LARGE-OP-CENTER-001` | `tests/large_operator_limits.rs` |
| `P-LATEX-MATH-ITALIC-001` | `tests/default_math_italic.rs`, `tests/row_math_italic.rs` |
| `P-LUALATEX-MATH-ORACLE-001` | `documents/MATH_ORACLE.md`, `tests/math_oracle.rs`, `tools/math_oracle.py`, `tools/math_compare.lua` |
| `P-TTF-SSTY-001` | `tests/script_style_alternates.rs`, `tests/script_glyph_scale.rs` |
| `P-LATEX-DELIMITER-SIZING-001` | `tests/delimiter_sizing.rs` |
| `P-LATEX-ACCENT-NUCLEUS-WIDTH-001` | `tests/accent_nucleus_width.rs` |
| `P-LATEX-SCRIPT-SPACE-001` | `tests/script_space_after.rs` |
| `P-OPENTYPE-SCRIPT-PLACEMENT-001` | `tests/script_placement.rs` |
| `P-AMSMATH-GRID-001` | `tests/amsmath_grid.rs` |
| `P-AMSMATH-SUBSTACK-001` | `tests/amsmath_substack.rs` |
| `P-LATEX-NESTED-ACCENT-001` | `tests/nested_accent_geometry.rs` |
| `P-LATEX-INTEGRAL-SCRIPTS-001` | `tests/integral_scripts.rs` |

---

## Archived pre-1.2.0 record

# Mathematical provenance and compatibility contracts

Paths are relative to this crate. Historical findings and limits remain in force.
The final public output includes composition repairs.

## Repair index

The links below identify the canonical explanation for each repair. Update and removal policy lives in [the audit contract](#c-latex-rust-compat-audit-001).

| Repair | Contract |
| --- | --- |
| [LR-DEFAULT-MATH-ITALIC-000](../src/ast.rs) | Mapeo de variables: contrato junto a la implementación. |
| [LR-WIDE-ACCENT-001](#p-latex-wide-accent-001) | Acentos hat y tilde. |
| [LR-RADICAL-VARIANT-002](#p-latex-radical-join-001) | Selección de variante radical. |
| [LR-RADICAL-JOIN-003](#p-latex-radical-join-001) | Unión entre radical y barra. |
| [LR-RADICAL-DEGREE-004](#p-latex-radical-degree-001) | Posición del índice radical. |
| [LR-FRACTION-NULL-DELIM-005](#p-latex-fraction-null-delim-001) | Espacio de delimitadores nulos. |
| [LR-DELIMITER-SIZING-006](#p-latex-delimiter-sizing-001) | Tamaño de delimitadores. |
| [LR-LARGE-OP-LIMITS-007](#p-latex-large-op-limits-001) | Límites de operadores. |
| [LR-MATH-ITALIC-008](#p-latex-math-italic-001) | Corrección itálica en filas. |
| [LR-SCRIPT-ALTERNATES-009](#p-ttf-ssty-001) | Alternativas tipográficas de índices. |
| [LR-SCRIPT-GLYPH-SCALE-010](../src/metrics.rs) | Escala del glifo: contrato junto a la implementación. |
| [LR-ACCENT-NUCLEUS-WIDTH-011](#p-latex-accent-nucleus-width-001) | Ancho del núcleo acentuado. |
| [LR-SCRIPT-SPACE-012](#p-latex-script-space-001) | Espacio posterior al índice. |
| [LR-LARGE-OP-AXIS-013](#p-latex-large-op-center-001) | Eje de operadores grandes. |
| [LR-LARGE-OP-RECENTER-014](#p-latex-large-op-center-001) | Recentrado de límites. |
| [LR-SCRIPT-PLACEMENT-015](#p-opentype-script-placement-001) | Posición de índices. |
| [LR-AMSMATH-GRID-016](#p-amsmath-grid-001) | Matrices, cases y aligned. |
| [LR-AMSMATH-SUBSTACK-017](#p-amsmath-substack-001) | Substack. |
| [LR-NESTED-ACCENT-GEOMETRY-018](#p-latex-nested-accent-001) | Acentos anidados. |
| [LR-INTEGRAL-SCRIPTS-019](#p-latex-integral-scripts-001) | Índices de integrales. |

## P-LATEX-WIDE-ACCENT-001

Kind: dependency-bug workaround plus TeX/OpenType MATH accent adaptation; no source copied.

External sources:
- `latex-rust` `1.0.1`, `src/layout/engine.rs`, especially `accent`, `accent_glyph`,
  `accent_raise`, `stretch_h`, and `accent_candidates`.
- OpenType MATH specification: `accentBaseHeight`, `MathTopAccentAttachment`, and horizontal
  `MathVariants`.
- TeX math-accent algorithm (Appendix G rule 12): advance to a larger accent successor only while
  that successor is no wider than the accentee, and preserve the accentee's final box width.

Relevant facts:
- `latex-rust` `1.0.1` resolves both `Hat` and `WideHat` from spacing U+02C6 first, and both
  `Tilde` and `WideTilde` from spacing U+02DC first.
- Those spacing glyphs are not the roots of STIX Two Math's horizontal MATH constructions. The
  combining U+0302/U+0303 glyphs expose the `circumflex.s*` / `tilde.s*` variants.
- `latex-rust` therefore cannot reach the font-designed wide variants from the glyph id it selected.
- Its spacing-accent vertical path also treats `accentBaseHeight` as a baseline raise by using
  `max(base_height, accentBaseHeight)`. OpenType defines `accentBaseHeight` instead as the maximum
  base ink height that needs no accent raise; the required raise is the excess above that threshold.
  Reusing the full base height double-counts the accent glyph's own positive y extents and visibly
  detaches the mark from capitals such as italic `J`.
- OpenType MATH supplies top-accent attachment points for horizontal placement; when either side has
  no attachment record, the advance-width center is the specified fallback.
- TeX's math-accent rule deliberately keeps the accented atom's width equal to the accentee width;
  font-designed variants are selected, not geometrically squeezed to fit.

latex-rust-fixes adaptation:
- Preserve `latex-rust` parsing, atom spacing, scripts, and the typed `MathBox`/display-list path.
- Track only hat/tilde accent kinds from the AST so the corresponding overlap can be repaired
  unambiguously after dependency layout.
- Repair vertical placement for both fixed and wide hat/tilde accents with
  `max(base_height - accentBaseHeight, 0)` at the exact current math-style scale.
- Align a single-glyph base and the selected accent through OpenType MATH top-accent attachment
  points. Composite bases and glyphs without an attachment record fall back to advance-width
  centers.
- For `\widehat` / `\widetilde`, use the combining glyph only to discover STIX Two Math's horizontal
  construction. Keep the ordinary spacing glyph as the smallest candidate and select the largest
  font-designed successor whose advance still fits the accentee, matching TeX's successor rule.
- Do not horizontally scale accent outlines. The accented atom retains the width already reserved
  by `latex-rust`, so subscripts, superscripts, and following atoms do not move.
- Because the upstream box can retain the old detached accent's empty top band, recompute the
  primitive vertical extent only for formulas that actually enter this repair path and remove that
  stale band from the inline-object metrics.
- The temporary independent x/y outline-scaling support from the first workaround was removed once
  font-designed, non-distorted variants became the invariant.

Crate targets:
- `src/accents.rs`
- `src/compose.rs`

Verification:
- `\hat J` and `\widehat J` use `accentBaseHeight` for vertical placement and the STIX Two Math
  top-accent attachment of italic `J`.
- A single-letter `\widehat J` remains on the fixed spacing accent when the next MATH variant would
  exceed the accentee width.
- A multi-letter `\widehat{XYZ}` selects the largest font variant that fits, with no geometric
  outline scaling.
- Existing AST/layout synchronization remains fail-closed through `ComposeState::finish`.

Sources reviewed:
- https://docs.rs/crate/latex-rust/1.0.1/source/src/layout/engine.rs
- https://docs.rs/crate/latex-rust/1.0.1/source/src/font/mod.rs
- https://learn.microsoft.com/typography/opentype/spec/math
- https://arusson.github.io/tex-c/part48.html

## P-LATEX-RADICAL-JOIN-001

Kind: local geometry repair for upstream radical-layout mismatches; no source copied.

External sources:
- `latex-rust 1.0.1`, `src/layout/engine.rs`, `Engine::radical` and `sized_glyph`.
- OpenType MATH specification, radical constants and MathVariants semantics.
- Typst, `crates/typst-layout/src/math/radical.rs`, which follows the TeXbook radical-placement
  relation and redistributes slack from a discrete radical variant into the vertical gap.
- Embedded STIX Two Math radical variants/metrics used by latex-rust-fixes.

Relevant facts:
- `latex-rust 1.0.1` chooses a ready-made vertical `√` variant and keeps the original
  `radicalVerticalGap` when positioning the independently drawn overbar.
- Its variant-size request also adds `radicalExtraAscender` to the radicand span, gap and rule
  thickness. OpenType defines that constant as extra white space reserved *above* the radical, not
  as part of the minimum glyph span. With discrete STIX variants that extra request can therefore
  select the next, needlessly tall radical glyph.
- A discrete STIX Two Math variant can be taller than the minimum requested span. Aligning that
  glyph to the old rule position by lowering the entire surd makes its descender fall far below the
  formula baseline.
- TeX/Typst instead keep the radicand baseline fixed and redistribute the excess height into the
  radical gap:
  `gap = max(gap0, (surd_span - rule_thickness - radicand_span + gap0) / 2)`.
- The corrected surd ascent is `radicand_ascent + gap + rule_thickness`; the remaining part of the
  selected variant becomes the radical descent. `radicalExtraAscender` is then reserved above that
  corrected inner ascent.
- STIX Two Math's ready-made radical variants have a small right-side ink overhang beyond their
  advance, so once the surd top and rule top are vertically aligned the font naturally covers the
  horizontal seam. latex-rust-fixes does not add a guessed pixel overlap.

latex-rust-fixes adaptation:
- Recognize only the exact typed `MathBox` topology emitted by `latex-rust` for a radical:
  a `√` glyph immediately followed by an `Overlap` containing exactly the overbar rule and
  radicand, with zero wrapper shifts and rule width equal to the radicand-column width.
- Before display-list emission, re-select a ready-made STIX vertical variant for a top-level radical
  against `radicand_span + original_gap + rule_thickness`, deliberately excluding
  `radicalExtraAscender` from the MathVariants size target. Preserve the exact style scale and use
  the smallest ready-made variant that satisfies the target, or the tallest available fallback.
- Limit variant replacement to top-level radical atoms. Replacing a nested radical after an
  enclosing fraction, delimiter or script has already used its old vertical metrics would require
  re-running that parent's layout; latex-rust-fixes fails closed there rather than creating inconsistent
  geometry.
- Reconstruct the original MATH gap, rule thickness, radicand span, selected-surds span and
  extra-ascender directly from style-scaled `Dim` values already present in the tree.
- Redistribute vertical slack with the TeX/Typst relation above.
- Keep the radicand on the formula baseline; move the rule to the redistributed gap and place the
  surd at the baseline implied by the corrected ascent. Do not lower the entire surd to meet the old
  rule position.
- Preserve degree kerns and font-designed radical outlines. If variant re-selection changes the
  surd advance, recompute only the final top-level HList width from its typed children.
- Bottom-up compatibility repairs may refresh child widths and overlap extents, but they must
  preserve any positive vertical padding that upstream stored outside the structural overlap. This
  is essential for `RadicalExtraAscender`: it is excluded from variant selection yet retained as
  legitimate white space above the finished radical.
- Once a radical or radical degree is emitted, derive the corrected surd/rule/radicand geometry
  from the typed tree while retaining that legitimate extra-ascender padding; discard only bands
  made stale by the superseded surd placement. Accent-only formulas retain their separate
  conservative bottom-band policy.
- The surd/rule seam correction still applies recursively during the ordinary typed display-list
  traversal, including nested radicals whose variant itself was intentionally left unchanged.

Crate targets:
- `src/compose.rs`
- `src/radicals.rs`

Verification:
- `radical_variant_selection_excludes_extra_ascender_from_minimum_span` proves on
  `\sqrt{x^2+y^2}` that the upstream request crosses a STIX variant boundary only when
  `radicalExtraAscender` is incorrectly included, and that latex-rust-fixes returns to the smallest fitting
  ready-made variant.
- `radical_surd_top_meets_rule_across_stix_vertical_variants` covers plain, tall, indexed and
  fraction-bearing radicals. It checks that the selected STIX surd top meets the redistributed rule,
  that the emitted radical descent equals the TeX/Typst target, and that the descender remains
  inside `Layout.height`.
- `tools/verify.py math` remains the external LuaLaTeX + `unicode-math` differential oracle for final
  width/ascent/descent and makes unnecessary tall-radical selection or stale vertical bands
  observable if this repair regresses.

Sources reviewed:
- https://docs.rs/crate/latex-rust/1.0.1/source/src/layout/engine.rs
- https://learn.microsoft.com/en-us/typography/opentype/spec/math
- https://github.com/typst/typst/blob/main/crates/typst-layout/src/math/radical.rs

## P-LATEX-RADICAL-DEGREE-001

Kind: local geometry repair for upstream radical-degree placement; no source copied.

External sources:
- `latex-rust 1.0.2`, pinned release commit
  `b5391dd306a792a7327a0a76bfa84fb9827d77c5`, `Engine::radical`.
- OpenType MATH 1.9.1, `radicalKernBeforeDegree`, `radicalKernAfterDegree`, and the corrected
  definition of `radicalDegreeBottomRaisePercent` in terms of the complete radical-sign height
  (ascender + descender).
- LuaTeX `mlist.c`, `make_radical`, which computes `h = height(y) + depth(y)` for the radical sign
  and positions the degree relative to the bottom of that shifted sign.

Relevant facts:
- `latex-rust 1.0.2` computes `raise = enclosing_radical_height * percent` and stores that value
  directly in the degree box shift. Its enclosing height is not the same quantity as LuaTeX's
  complete shifted radical-sign span once a ready-made surd has non-zero corrected descent.
- LuaTeX's relation is equivalent, in latex-rust-fixes's positive-up coordinates, to placing the degree
  baseline `percent * surd_span` above the bottom of the shifted radical sign.
- Therefore the desired latex-rust-fixes shift is
  `surd_span * percent - corrected_radical_descent`.
- The degree box depth is not added to that shift. Adding it raises a tall degree twice; the
  LuaLaTeX differential exposed this directly for `\sqrt[\frac{1+\alpha}{2}]{x}` as roughly
  0.27 em of excess ascent.
- `radicalExtraAscender` is reserved white space above the finished radical, not part of the radical
  sign span used by the degree-raise percentage.
- Horizontal degree position remains governed by the font's MATH `radicalKernBeforeDegree` and
  `radicalKernAfterDegree`; no guessed horizontal offset is introduced.

latex-rust-fixes adaptation:
- Recognize only the exact five-child indexed-radical HList emitted by `latex-rust`: kern-before,
  degree, kern-after, surd, radicand-column.
- Reuse the corrected `surd_span` and radical descent produced by `P-LATEX-RADICAL-JOIN-001`.
- During display-list emission, replace only the degree's vertical shift with
  `surd_span * percent - corrected_descent`.
- Preserve both horizontal MATH kerns, the degree contents, the radicand baseline, and all
  surd/rule geometry.
- If the corrected degree genuinely protrudes above the upstream box, grow the final `Layout`
  upward rather than clipping it.

Crate targets:
- `src/compose.rs`
- `src/radicals.rs`

Verification:
- `radical_degree_baseline_follows_luatex_raise_formula` covers both a simple `17` degree and the
  compound `\frac{1+\alpha}{2}` degree. It computes each probe glyph's internal baseline offset in
  the repaired degree box and verifies the emitted baseline against the LuaTeX-equivalent shift.
- The same test separately proves that the surd x position — therefore the font's horizontal degree
  kern geometry — remains unchanged.
- `radical_surd_top_meets_rule_across_stix_vertical_variants` continues to verify the independent
  surd/overbar seam repair.
- `uv run tools/verify.py math` remains the independent LuaLaTeX + `unicode-math` oracle.

Sources reviewed:
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- https://learn.microsoft.com/en-us/typography/opentype/spec/math
- https://github.com/minux/luatex/blob/c357addd56b638e5a9926c5ac0dcbbcf6a6753dc/source/texk/web2c/luatexdir/tex/mlist.c

## C-LATEX-RUST-COMPAT-AUDIT-001

Kind: dependency compatibility contract; no source copied.

External source:
- `latex-rust` release commit `b5391dd306a792a7327a0a76bfa84fb9827d77c5`, whose package metadata declares version `1.0.2`.

Relevant facts:
- latex-rust-fixes carries local repairs for upstream layout behavior. A dependency update can therefore make a
  workaround obsolete, partially obsolete, or structurally unsafe even when the public API still
  compiles.
- The reviewed 1.0.2 release commit still contains the radical variant-selection, fraction
  null-delimiter, large-operator-limit, and wide-accent behaviors documented in the corresponding
  provenance entries.
- Git revision pinning is intentional because the audited 1.0.2 source is identified by commit, not
  merely by an unconstrained moving branch.

latex-rust-fixes policy:
- All upstream layout workarounds belong to this crate and are not duplicated outside its public composition path.
- `Cargo.toml` pins both expected package version and exact Git revision.
- `manifest_latex_rust_revision_matches_fix_audit` fails if either marker changes without updating
  the module's audited constants. Advancing those constants requires reviewing every `LR-*` entry
  and rerunning `uv run tools/verify.py math`.
- Workarounds are deleted, not retained defensively, once the pinned upstream revision demonstrably
  implements the same correction.
- Known divergences that cannot be repaired soundly from the post-layout `MathBox` topology remain
  explicitly deferred rather than being approximated by heuristics.

Crate targets:
- `Cargo.toml`
- `src/audit.rs`
- `src/regression_tests.rs`

Verification:
- ordinary Rust tests include the manifest/revision fuse;
- the LuaLaTeX matrix is rerun after every `latex-rust` update;
- Miri policy classifies the audit test and every new compatibility regression explicitly.

Sources reviewed:
- https://github.com/jscarr64/LaTeX-Rust/commit/b5391dd306a792a7327a0a76bfa84fb9827d77c5
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/Cargo.toml
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs

## P-LATEX-FRACTION-NULL-DELIM-001

Kind: TeX-compatibility repair for an upstream fraction-width omission; no source copied.

External sources:
- `latex-rust 1.0.2`, `Engine::fraction` in the pinned release commit.
- TeX generalized-fraction behavior and the default `\nulldelimiterspace = 1.2pt`.
- latex-rust-fixes's LuaLaTeX + `unicode-math` differential matrix using the exact same STIX Two Math bytes.

Relevant facts:
- `latex-rust` sets a fraction box width to `max(numerator.width, denominator.width)` and does not
  reserve the two null-delimiter spaces around a delimiter-less generalized fraction.
- LuaLaTeX consequently reports about 0.24 em more width for a display fraction at a 10 pt math em;
  nested fractions propagate the omission.
- `\nulldelimiterspace` is an absolute TeX dimension. Encoding the correction as a fixed `0.12em`
  would be correct only at 10 pt and would become wrong at other physical em sizes.

latex-rust-fixes adaptation:
- Use the physical em size supplied in TeX points to convert each absolute null-delimiter
  space to root-em units before dependency-layout repair.
- Recognize only the exact three-branch fraction overlap shape: positive-shift numerator, zero-depth
  rule spanning the upstream box, negative-shift denominator.
- Treat each numerator/denominator branch as an opaque semantic unit after bottom-up child fixes;
  re-center the complete branches to the refreshed common column width, widen the rule to match,
  then wrap the column with two physical `\nulldelimiterspace` kerns. Never unwrap branch HLists
  to infer whether internal symmetric spacing was user-authored or generated by the dependency.

Crate targets:
- `src/fractions.rs`

Verification:
- `fraction_null_delimiter_space_remains_physical_across_em_sizes` proves the total width addition is
  0.24 em at 10 pt and 0.12 em at 20 pt, i.e. a constant 2.4 physical points.
- `uv run tools/verify.py math` measures simple, display, nested and radical-contained fractions against
  LuaLaTeX.

Sources reviewed:
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- https://www.luatex.org/svn/trunk/manual/luatex.pdf

## P-LATEX-LARGE-OP-LIMITS-001

Kind: OpenType MATH large-operator limit-placement repair; no source copied.

External sources:
- `latex-rust 1.0.2`, `Engine::attach_limits`.
- OpenType MATH constants `UpperLimitGapMin`, `UpperLimitBaselineRiseMin`,
  `LowerLimitGapMin`, and `LowerLimitBaselineDropMin`.
- Typst `crates/typst-layout/src/math/scripts.rs`, `compute_limit_shifts`.

Relevant facts:
- The gap minimum constrains the edge-to-edge distance between operator and limit; the baseline
  rise/drop minimum constrains the limit baseline. They are independent inequalities.
- `latex-rust 1.0.2` computes `max(gap_min, baseline_min)` first and then adds the complete limit
  height/depth. This over-raises/over-drops limits; the LuaLaTeX display-sum probe exposed an excess
  lower depth of roughly 0.467 em.
- The correct upper shift is `operator_ascent + max(baseline_rise_min, gap_min + limit_depth)`; the
  lower relation is symmetric with operator descent and limit ascent.

latex-rust-fixes adaptation:
- Recognize only an overlap whose first visible leaf is a known large operator and whose remaining
  branches already have signed limit shifts.
- Replace only those vertical shifts and recompute the enclosing overlap height/depth. Preserve
  upstream horizontal centering.
- Propagate this repair only through a top-level row; do not cross fractions, radicals, script slots,
  or semantic-fence-like rows whose parents were positioned from the old vertical metrics.

Crate targets:
- `src/operators.rs`

Verification:
- `large_operator_limit_repair_reduces_upstream_excess_depth` guards the upstream failure mode.
- `display-sum` in `uv run tools/verify.py math` remains the independent LuaLaTeX oracle.

Sources reviewed:
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- https://learn.microsoft.com/typography/opentype/spec/math
- https://github.com/typst/typst/blob/main/crates/typst-layout/src/math/scripts.rs

## P-LATEX-MATH-ITALIC-001

Kind: TeX/OpenType math-italic width repair for upstream row packing; no source copied.

External sources:
- `latex-rust 1.0.2`, glyph creation, row packing and script attachment in `Engine`.
- OpenType MATH italic-correction values from the same embedded STIX Two Math face.
- latex-rust-fixes's LuaLaTeX differential measurements for ordinary variables and wide-accent nuclei.

Relevant facts:
- `latex-rust` stores a glyph's MATH italic correction in `MathBox::italic`, but generic `row()`
  packs only glyph advances and inter-atom spacing. The field is consumed specially for superscript
  attachment and otherwise disappears from horizontal row geometry.
- This produces small systematic width deficits for ordinary math-italic rows and larger cumulative
  deficits for multi-letter nuclei such as `XYZ`.
- Script attachment must not receive the correction twice.

latex-rust-fixes adaptation:
- Before structural compatibility repairs, walk typed boxes bottom-up and append the stored italic
  correction after every default math-italic glyph in an ordinary row. This follows TeX section 755:
  when the nucleus is a math character and there is no subscript, the italic kern is appended even
  when that noad is the final item in the row.
- Skip the exact centering wrappers and script-attachment HLists emitted by `latex-rust`; the latter
  are recognized by their shifted overlap slot, optional explicit italic kern, and optional trailing
  `space_after_script` kern. This prevents the compatibility pass from adding the base italic
  correction a second time in the four-child superscript form.
- Recompute only the affected HList metrics. No glyph metrics or outlines are modified.

Crate targets:
- `src/scripts.rs`

Verification:
- `row_math_italic_correction_matches_tex_no_subscript_rule` derives its expected width
  delta from the embedded font's own italic-correction fields.
- `text-simple` and wide-accent cases in `uv run tools/verify.py math` provide the independent LuaLaTeX
  comparison.

Sources reviewed:
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- https://learn.microsoft.com/typography/opentype/spec/math
- TeX `mlist_to_hlist`, section 755 (math-character italic-correction kern insertion).

## P-LUALATEX-MATH-ORACLE-001

Kind: external differential-test oracle; no production dependency and no source copied.

External sources:
- LuaTeX reference manual, node/list box dimensions and Lua node API.
- `unicode-math`, OpenType math-font loading through `\setmathfont` under LuaLaTeX.
- pinned `latex-rust` release commit; exact embedded STIX Two Math bytes exported only into the temporary oracle directory.

Relevant facts:
- LuaTeX exposes the final `hbox` width, height and depth in scaled points, so mathematical layout
  can be compared before PDF rasterization, antialiasing and device-pixel rounding.
- `unicode-math` accepts an OpenType math font by filename. The harness therefore uses the exact
  OTF bytes embedded by latex-rust-fixes's pinned `latex-rust`, rather than trusting a same-named system font.
- latex-rust-fixes's `Layout` and LuaTeX box dimensions are normalized by their base math em before
  comparison. The baseline profile remains at 10 pt, while the stress profile additionally sweeps
  selected formulas at 6, 10, 20 and 40 pt so physical TeX dimensions cannot accidentally agree at
  one size.
- `unicode-math` derives `\DeclareMathSizes` from the OpenType MATH `ScriptPercentScaleDown` and
  `ScriptScriptPercentScaleDown` values for the font size active when `\setmathfont` is configured.
  A later arbitrary `\fontsize` is not by itself a proof that LaTeX selected that exact math text
  size. The oracle therefore exports the two percentages from latex-rust-fixes's `MathParams`, emits an
  explicit `\DeclareMathSizes` for every requested physical size. A formula under test is not
  required to contain a root-size glyph: for example, `\frac{1}{2}` in text style legitimately
  contains only scriptstyle numerator/denominator glyphs. The oracle therefore typesets a separate
  one-glyph `x` control box at the same selected math size and rejects a Lua result unless that
  control glyph matches the requested root math em within two scaled points. This prevents both a
  LaTeX size-declaration substitution and legitimate internal script sizing from masquerading as an
  latex-rust-fixes scaling defect.
- LuaTeX's internal hlist/vlist decomposition is not required to match latex-rust-fixes's typed display list.
  Glyph/rule counts are retained only as diagnostic structural evidence; width/ascent/descent are
  the primary cross-engine geometry observables.

latex-rust-fixes adaptation:
- `tests/math_oracle.rs::lualatex_math_comparison_probe` is ignored in ordinary `cargo test`. It exports the
  embedded font and emits a curated set of text/display formulas covering basic atoms, scripts,
  fractions, delimiters, operators, radicals, radical degrees and repaired wide accents.
- `uv run tools/verify.py math` invokes the Rust probe, builds one LuaLaTeX document over the identical
  formula/style/physical-size corpus, parses machine-readable Lua results, prints per-case and
  per-family deltas in the terminal without persisting a report.
- The ordinary profile stays intentionally small for release gating. `--stress` adds the curated
  73-case torture corpus committed in `tests/fixtures/math_compare_stress.tsv`, for 94 total cases
  including the 21-case baseline. It exercises deep scripts, nested fractions/radicals, automatic
  and explicit delimiters, long/nested accents, limit stacks, integrals, matrices, cases/aligned
  boxes, phantom geometry, tensor/calculus expressions and a four-size physical-dimension sweep.
- Stress summaries include nearest-rank p50/p90/p95/p99/max deltas, maxima by family and physical
  size, structural glyph/rule mismatches, and the worst cases, so regressions are visible even when
  all cases remain below the binary tolerance threshold.
- `tools/math_compare.lua` inspects final TeX boxes directly and measures the root math em from a
  separate one-glyph control box at the same physical size. Internal script/script-script glyphs in
  the formula under test therefore cannot be mistaken for the root size. It never parses
  PDF/SVG/raster output.
- A default 0.05 em threshold classifies diagnostic divergence. The comparison remains diagnostic-only
  by default; `--fail-on-delta` turns the same
  threshold into an explicit gate when a reviewed baseline warrants it. The stress profile is
  deliberately diagnostic first: percentile and worst-case movement matter even below 0.05 em.

Not adopted:
- Pixel-by-pixel screenshot/PDF comparison as the normative oracle.
- An installed STIX Two Math family selected only by name.
- LuaLaTeX or `unicode-math` in latex-rust-fixes production code.
- Treating LuaTeX node counts as semantic equality requirements.

Crate targets:
- `tests/math_oracle.rs`
- `tests/fixtures/math_compare_stress.tsv`
- `uv run tools/verify.py math`
- `tools/math_compare.lua`

Verification:
- The ordinary Rust suite remains independent of LuaLaTeX because the probe is ignored.
- Running `uv run tools/verify.py math` must produce one LuaLaTeX result for every latex-rust-fixes case and complete the in-memory geometry comparison; `--stress` must additionally load the bounded stress fixture and emit the distribution/size summaries. Every requested physical size
  must be backed by an explicit `\DeclareMathSizes` built from the embedded font's reported MATH
  percentages, and Lua node inspection of the separate root-size control box must confirm the
  requested math text em before comparison.
- The oracle uses the exact exported font bytes from the Rust probe; generated font and TeX files remain inside the temporary run directory and are removed afterwards.

Sources reviewed:
- https://www.luatex.org/svn/trunk/manual/luatex.pdf
- https://ctan.org/pkg/unicode-math
- https://tug.ctan.org/macros/unicodetex/latex/unicode-math/unicode-math-code.pdf
- https://github.com/jscarr64/LaTeX-Rust/commit/b5391dd306a792a7327a0a76bfa84fb9827d77c5


## P-TTF-SSTY-001

Kind: OpenType GSUB script-style alternate lookup through `ttf-parser`; no source copied.

External sources:
- OpenType registered `ssty` feature semantics for mathematical Script and ScriptScript alternates.
- `ttf-parser 0.25.1` GSUB `AlternateSubstitution`, feature-list and lookup APIs.
- STIX Two Math `ssty` table contained in the exact font bytes embedded by `latex-rust 1.0.2`.

Relevant facts:
- The MATH ScriptPercentScaleDown and ScriptScriptPercentScaleDown constants scale glyph geometry,
  while the `ssty` GSUB feature can additionally substitute optically designed glyphs.
- STIX Two Math exposes the first `ssty` alternate for Script and the second for ScriptScript.
- `latex-rust 1.0.2` applies only the MATH scale and retains the default glyph id, producing small
  but systematic width/height differences in superscripts, radical degrees and nested fractions.

latex-rust-fixes adaptation:
- Parse the already embedded font bytes with safe `ttf-parser` while constructing the persistent
  repair environment; locate `ssty` and materialize only source glyphs that have Script or
  ScriptScript alternates into a sorted sparse lookup, without a handwritten glyph-id table.
- Formula repair queries that persistent lookup instead of reparsing GSUB for every expression.
- Infer Script/ScriptScript only from the exact scale already encoded in each `MathBox` glyph,
  replace the glyph id with the corresponding STIX alternate, and rebuild metrics from the font.
- Run this before row italic correction so the alternate's own MATH italic correction is used.

Crate targets:
- `src/scripts.rs`

Verification:
- `script_style_uses_open_type_ssty_alternate` compares the persistent sparse lookup against direct
  `ttf-parser` GSUB lookup for every embedded glyph at Script and ScriptScript levels, then proves
  that an actual STIX `ssty` alternate replaces the default digit glyph in a script box.
- `uv run tools/verify.py math` independently checks script, nested-fraction and radical-degree geometry.

Sources reviewed:
- https://learn.microsoft.com/typography/opentype/spec/features_pt#ssty
- https://docs.rs/ttf-parser/0.25.1/ttf_parser/gsub/index.html
- https://github.com/harfbuzz/ttf-parser/tree/v0.25.1/src

## P-LATEX-DELIMITER-SIZING-001

Kind: TeX delimiter sizing and axis-centering repair for `latex-rust 1.0.2`; no source copied.

External sources:
- LuaTeX `get_delimiter_height` implementation and default TeX delimiter parameters.
- OpenType MATH vertical MathVariants metrics from the embedded STIX Two Math face.
- `latex-rust 1.0.2` `Engine::delimited` and `sized_glyph` implementation.

Relevant facts:
- TeX computes a required delimiter size from the maximum distance to the math axis and applies both
  `delimiterfactor` (901 by default) and the absolute `delimitershortfall` (5 pt by default).
- `latex-rust 1.0.2` instead requests exactly twice the maximum axis distance. For a display
  fraction in STIX this crosses into the next ready-made parenthesis variant.
- The chosen delimiter is centered on the math axis; the glyph's raw bbox is not itself the final
  formula ascent/descent.

latex-rust-fixes adaptation:
- Apply this repair only when the parsed root semantic node is actually `MathNode::Delimited` (or a
  singleton root row containing it). Never infer `\\left...\\right` from a generic HList shape.
- Preserve `delimitershortfall` as a physical 5 pt quantity by resolving it against the runtime root
  em size, select the smallest fitting STIX vertical variant, and center it on the MATH axis.
- Recompute the semantic fence HList with child shifts included in vertical extents.

Crate targets:
- `src/delimiters.rs`

Verification:
- `semantic_delimiter_repair_selects_tex_sized_variant` exercises a display fraction inside
  `\\left(...\\right)` and requires the corrected geometry to shrink from the upstream variant.
- `display-delimited` in `uv run tools/verify.py math` is the independent LuaLaTeX oracle.

Sources reviewed:
- LuaTeX `source/texk/web2c/luatexdir/tex/mlist.c`, `get_delimiter_height`.
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- https://learn.microsoft.com/typography/opentype/spec/math

## P-LATEX-ACCENT-NUCLEUS-WIDTH-001

Kind: TeX/OpenType accent wrapper-width repair for `latex-rust 1.0.2`; no source copied.

External sources:
- TeX `make_math_accent` box construction.
- OpenType MATH italic-correction metrics from the exact embedded STIX Two Math face.
- `latex-rust 1.0.2` `overlay_accent` implementation.

Relevant facts:
- TeX lets the accent overhang and gives the final accent box the width of the nucleus.
- A direct mathematical-italic nucleus includes its italic-correction kern in that effective width.
- `latex-rust` instead uses `max(nucleus_width, accent_width)` and clears the wrapper italic value.
  For STIX mathematical italic J this makes `\\widehat J` 0.398 em instead of 0.458 em; the missing
  0.060 em is exactly the font's MATH italic correction.

latex-rust-fixes adaptation:
- Restrict the width correction to the already validated two-branch hat/tilde overlap topology.
- Direct glyph nuclei use advance plus their MATH italic correction. Composite nuclei retain their
  repaired row width, which already contains LR-MATH-ITALIC-008 kerns.
- Accent rendering/placement itself remains governed by LR-WIDE-ACCENT-001.

Crate targets:
- `src/repair.rs`

Verification:
- `hat_tilde_overlay_width_follows_nucleus_italic_advance` derives the expected width directly from
  STIX's own advance and italic-correction values.
- `accent-hat-j`, `accent-widehat-j`, `accent-widehat-xyz` and `accent-widetilde-xyz` remain in the
  LuaLaTeX differential corpus.

Sources reviewed:
- TeX `make_math_accent`, section 738-742.
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- https://learn.microsoft.com/typography/opentype/spec/math


## P-LATEX-SCRIPT-SPACE-001

Kind: OpenType MATH `SpaceAfterScript` style-scaling repair for `latex-rust 1.0.2`; no source copied.

External sources:
- OpenType MATH `SpaceAfterScript` constant semantics.
- LuaTeX/unicode-math node geometry for Script glyphs in the exact STIX Two Math oracle.
- `latex-rust 1.0.2` `Engine::attach_scripts_to_box` implementation.

Relevant facts:
- `SpaceAfterScript` is spacing after a script attachment in the current (parent) math style.
- For a 10 pt text-style `i^2`, LuaLaTeX retains 0.040 em after the Script glyph while the glyph
  itself is optically substituted/scaled to Script style.
- `latex-rust 1.0.2` computes `SpaceAfterScript * scale(style.into_script())`; with STIX this emits
  0.028 em instead of 0.040 em at root text/display style, a deterministic 0.012 em deficit.

latex-rust-fixes adaptation:
- Recognize only the exact audited script-attachment HList topology already used to protect
  LR-MATH-ITALIC-008.
- Recover the parent scale from a single-glyph base after `ssty` substitution and replace only the
  trailing script-space kern. Complex bases fail closed rather than guessing a style.
- Run the repair after `ssty` and before row italic correction/structural metric propagation.

Crate targets:
- `src/scripts.rs`

Verification:
- `script_space_after_uses_parent_style_scale` checks the exact missing
  `SpaceAfterScript * (1 - ScriptPercentScaleDown)` delta.
- `text-superscript`, `text-scripts`, `radical-tall`, `accent-widehat-script` and `display-sum` in
  the LuaLaTeX differential corpus exercise the spacing in independent parents.

Sources reviewed:
- https://learn.microsoft.com/typography/opentype/spec/math
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- LuaTeX `source/texk/web2c/luatexdir/tex/mlist.c`.

## P-LATEX-LARGE-OP-CENTER-001

Kind: display-operator re-centering and MATH-axis alignment repair for the post-layout
`latex-rust 1.0.2` compatibility pipeline; no source copied.

External sources:
- LuaTeX `make_op` displayed-limit construction.
- OpenType MATH `AxisHeight` and STIX MathVariants operator metrics.
- `latex-rust 1.0.2` `Engine::large_op`, `attach_limits` and `center_in` implementation.

Relevant facts:
- LuaTeX chooses the common width from the final operator, upper-limit and lower-limit boxes, then
  reboxes all three to that width. It also centers the enlarged operator nucleus on the math axis.
- `latex-rust` centers the branches before latex-rust-fixes can apply the missing STIX `ssty` substitutions.
  When `i=1` grows to its Script alternates, the old symmetric centering kerns remain and inflate
  the displayed-sum width even though they no longer represent centering.
- Stale centering padding can therefore inflate displayed-sum width after `ssty` substitution,
  independently of the separate `SpaceAfterScript` correction.

latex-rust-fixes adaptation:
- Only inside an overlap already proven to be a large operator with signed limit branches, unwrap
  the exact symmetric `center_in` wrappers, recompute the maximum intrinsic branch width after all
  glyph repairs, and center the branches again.
- Shift the operator nucleus so `(height - depth)/2 + shift == AxisHeight` before applying the
  independent upper/lower limit constraints from LR-LARGE-OP-LIMITS-007.
- Generic HLists are never unwrapped; the correction is scoped to the recognized operator topology.

Crate targets:
- `src/operators.rs`

Verification:
- `large_operator_repair_discards_stale_ssty_centering` requires the outer operator width to equal
  the maximum repaired intrinsic branch width and the operator center to land exactly on AxisHeight.
- `display-sum-limits` and `display-sum` provide independent LuaLaTeX geometry checks.

Sources reviewed:
- LuaTeX `source/texk/web2c/luatexdir/tex/mlist.c`, `make_op`.
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
- https://learn.microsoft.com/typography/opentype/spec/math

## P-OPENTYPE-SCRIPT-PLACEMENT-001

Kind: OpenType MATH script-placement compatibility repair for `latex-rust 1.0.2`; no source copied.

External sources:
- OpenType MATH table script-placement constants.
- LuaTeX `make_scripts` new-math implementation.
- `latex-rust 1.0.2` `Engine::attach_scripts_to_box` implementation.

Relevant facts:
- For a simple-character nucleus, OpenType MATH requires more than the nominal
  `SuperscriptShiftUp`, `SubscriptShiftDown` and `SubSuperscriptGapMin`: the superscript bottom
  must satisfy `SuperscriptBottomMin`, the subscript top must satisfy `SubscriptTopMax`, and a
  paired sub/superscript can additionally require `SuperscriptBottomMaxWithSubscript` after the
  minimum-gap correction.
- LuaTeX's new-math `make_scripts` applies those constraints in that order. Its baseline-drop
  parameters are used when the nucleus has been boxed; a direct character nucleus starts with zero
  drop contribution instead.
- `latex-rust 1.0.2` starts directly from the nominal shifts, applies only the minimum sub/sup gap,
  and therefore underestimates vertical extents for combinations such as `x_i^2` and recursively
  nested scripts.

latex-rust-fixes adaptation:
- Repair only the already audited script-attachment HList/Overlap topology.
- Recover the parent math scale only from a direct single-glyph nucleus, infer normal versus cramped
  superscript placement from the untouched upstream shift, and apply the missing MATH limits.
- Process the tree bottom-up so a repaired nested script contributes its final metrics to the
  containing script. Complex/boxed nuclei deliberately fail closed; their baseline-drop rules are
  not guessed from topology.
- Preserve horizontal script geometry, `ssty`, italic correction and `SpaceAfterScript` as separate
  compatibility repairs.

Crate targets:
- `src/scripts.rs`

Verification:
- `script_placement_enforces_missing_math_constraints` requires both ascent and depth of `x_i^2`
  to increase when the missing constraints are applied.
- `superscript_only_stays_stable_when_existing_shift_satisfies_math_constraints` protects the
  already-converged `i^2` case from unnecessary movement.
- The stress oracle cases `text-scripts`, `hard-script-deep`, `hard-script-extreme`,
  `hard-script-boxes` and `hard-script-on-delimited` provide independent LuaLaTeX measurements.

Sources reviewed:
- https://learn.microsoft.com/typography/opentype/spec/math
- https://github.com/minux/luatex/blob/master/source/texk/web2c/luatexdir/tex/mlist.c (`make_scripts`)
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs (`attach_scripts_to_box`)

## P-AMSMATH-GRID-001

Kind: AMSMath matrix/cases/aligned semantic-layout compatibility repair for `latex-rust 1.0.2`; no source copied.

External sources:
- LaTeX kernel `classes.dtx` array spacing defaults.
- LaTeX kernel `ltmath.dtx` `\jot` default and `ltplain.dtx` normal line-skip defaults.
- AMSMath `amsmath.dtx` implementations of `\env@matrix`, `cases`, `aligned` and `\spread@equation`.
- `latex-rust 1.0.2` `Engine::grid`, `centered_matrix`, `cases_env` and `align_env` implementations.

Relevant facts:
- Standard LaTeX classes define `\arraycolsep=5pt`; adjacent array columns therefore receive
  `2\arraycolsep`, while AMSMath's `\env@matrix` removes only the two outside half-spaces.
- Matrix/array cells are independent text-style math lists. `cases` is specifically
  `\array{@{}l@{\quad}l@{}}` with `\arraystretch=1.2`.
- `aligned` explicitly lays out cells in `\displaystyle`, prefixes every right-hand field with
  an empty Ord group (`${}##`), uses a strut in every row, defaults `\minalignsep` to 10pt between
  alignment pairs, and calls `\spread@equation`, whose `\openup\jot`
  uses the LaTeX kernel default `\jot=3pt`. The kernel defaults `\normallineskip=1pt` and
  `\normallineskiplimit=0pt`; after `\openup\jot`, aligned inter-row glue is therefore chosen
  by TeX from the enlarged baseline skip or enlarged line skip according to the enlarged line-skip
  limit, rather than being a fixed `0.3em` separator.
- The default `aligned` placement and the array-based matrix/cases structures are vertically
  centered relative to the surrounding math axis. `latex-rust 1.0.2` instead leaves the VList
  baseline at the first row and uses a generic 0.2em separator.
- The differential oracle deliberately selects a text baseline equal to its requested font size;
  its normal strut therefore contributes 0.7em height and 0.3em depth, with the cases stretch
  multiplying those values by 1.2.

latex-rust-fixes adaptation:
- Rebuild only AST-identified `matrix`, `pmatrix`, `bmatrix`, `vmatrix`, `Vmatrix`, `Bmatrix`,
  `cases` and `aligned`; `array`, `split`, numbered display environments, `hline` and `intertext`
  retain the upstream tree until their independent semantics are audited.
- Re-layout each matrix/cases cell in text style and each aligned cell in display style,
  recursively applying the already-audited compatibility repairs to the cell before packing. For
  right-hand aligned fields, derive the `${}##` leading-Ord spacing through `latex-rust`'s own
  atom-spacing engine instead of hard-coding a mu width.
- Insert zero-width strut boxes, use the documented physical column dimensions, and reproduce
  `aligned` inter-row glue from the baseline-skip/line-skip decision after `\openup\jot`; center
  the complete row stack on `AxisHeight`, and size matrix/cases delimiters with the existing
  audited TeX delimiter factor/shortfall rule.
- No stress-case dimensions are hard-coded; every value comes from LaTeX/AMSMath defaults,
  OpenType MATH metrics, the parsed AST or the requested physical em size.

Crate targets:
- `src/environments.rs`

Verification:
- `semantic_matrix_relayout_uses_tex_array_spacing_and_axis_center` checks the wider 5pt+5pt
  inter-column geometry and exact math-axis centering of a 3x3 `bmatrix`.
- `semantic_cases_relayout_uses_textstyle_cells` protects the text-style cell rule and vcenter.
- `semantic_aligned_relayout_centers_complete_stack` protects display-style aligned rows and
  complete-stack axis centering.
- `semantic_aligned_relayout_applies_empty_ord_right_field_preamble` protects the exact `${}##`
  leading-Ord atom-spacing semantics of right-hand alignment fields.
- Stress-oracle cases `hard-matrix-fractions`, `hard-matrix-3x3`, `hard-determinant`, `hard-cases`,
  `hard-aligned` and `hard-aligned-model` provide independent LuaLaTeX measurements.

Sources reviewed:
- https://github.com/latex3/latex2e/blob/2dbf26798d7c0a3101eee6d0c78c142d89412d67/base/classes.dtx
- https://github.com/latex3/latex2e/blob/2dbf26798d7c0a3101eee6d0c78c142d89412d67/base/ltmath.dtx
- https://github.com/latex3/latex2e/blob/2dbf26798d7c0a3101eee6d0c78c142d89412d67/base/ltplain.dtx
- https://github.com/latex3/latex2e/blob/2dbf26798d7c0a3101eee6d0c78c142d89412d67/required/amsmath/amsmath.dtx
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs

## P-AMSMATH-SUBSTACK-001

Kind: AMSMath `substack`/`subarray` compatibility repair for `latex-rust 1.0.2`; no source copied.

External sources:
- AMSMath `amsmath.dtx` implementation of `subarray` and `\substack`.
- LuaTeX reference manual mapping of `\Umathstacknumup`, `\Umathstackdenomdown` and
  `\Umathstackvgap` to OpenType MATH stack constants.
- OpenType MATH `StackTopShiftUp`, `StackBottomShiftDown` and `StackGapMin` definitions.
- `latex-rust 1.0.2` `Engine::substack` and `Engine::attach_limits` implementations.

Relevant facts:
- `\substack` is an abbreviation for a centered one-column `subarray`.
- AMSMath always lays every `subarray` field in `\scriptstyle`; it explicitly does not descend to
  `\scriptscriptstyle`. The LuaTeX branch sets the row baseline skip to
  `\Umathstacknumup\scriptstyle + \Umathstackdenomdown\scriptstyle`, sets `\lineskip` and
  `\lineskiplimit` to `\Umathstackvgap\scriptstyle`, and wraps the alignment in `\vcenter`.
- LuaTeX maps those Script-style primitives to OpenType MATH `StackTopShiftUp`,
  `StackBottomShiftDown` and `StackGapMin`, respectively.
- `latex-rust 1.0.2` instead calls `style.into_script()` inside `Engine::substack`, separates rows by
  a fixed `0.2em`, and returns a `vpack` whose baseline remains on the first row. When `substack`
  is already a display-operator limit, `attach_limits` has first moved the limit to Script style;
  the additional `into_script()` therefore incorrectly shrinks the substack rows to ScriptScript.

latex-rust-fixes adaptation:
- Re-layout every AST-identified substack row in fixed `MathStyle::Script`, center rows to the
  widest row, derive baseline skip and fallback line skip from the font's OpenType MATH constants,
  apply TeX's baseline-skip/line-skip decision between adjacent rows, and vcenter the complete
  stack on the surrounding style's math axis.
- Encapsulate the vcenter shift inside a one-child HList so an enclosing display operator can apply
  its independent upper/lower-limit shift without overwriting the substack's internal baseline.
- Rebuild only an AST-root `Substack` or a `Substack` used directly as a display `Sum`/`Product`
  limit when that operator is itself the root or a direct top-level Row child. More deeply nested
  contexts remain upstream until their parent geometry has an independently audited relayout path.
- No stress-case dimensions are hard-coded; all vertical quantities come from OpenType MATH and
  all row widths come from recursively repaired Script-style layout.

Crate targets:
- `src/environments.rs`

Verification:
- `semantic_substack_uses_scriptstyle_rows_and_math_vcenter` proves that an outer Script substack
  does not collapse its rows to ScriptScript and that the complete stack is centered on the Script
  math axis.
- `semantic_display_sum_rebuilds_direct_substack_limit` proves that a top-level display sum adopts
  the repaired substack width before large-operator limits are re-centered and re-positioned.
- Stress-oracle cases `hard-sum-substack` and `hard-sum-substack-extreme` provide independent
  LuaLaTeX geometry measurements.

Sources reviewed:
- https://github.com/latex3/latex2e/blob/2dbf26798d7c0a3101eee6d0c78c142d89412d67/required/amsmath/amsmath.dtx
- https://www.luatex.org/svn/trunk/manual/luatex.pdf
- https://learn.microsoft.com/typography/opentype/spec/math
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs

## P-LATEX-NESTED-ACCENT-001

Kind: nested hat/tilde OpenType MATH geometry repair for `latex-rust 1.0.2`; no source copied.

External sources:
- LuaTeX `mlist.c` `do_make_math_accent` and nested-accent skew handling.
- OpenType MATH `AccentBaseHeight` and top-accent attachment definitions.
- `latex-rust 1.0.2` `Engine::accent`, `Engine::accent_raise` and `overlay_accent` implementations.

Relevant facts:
- LuaTeX lays out the accent nucleus in cramped style and raises a top accent only by the amount
  that the nucleus height exceeds `AccentBaseHeight`.
- A nested accent is a genuine base for the next outer accent; LuaTeX recursively aligns stacked
  accents to the innermost accent noad and therefore uses the completed inner accent geometry when
  constructing the next layer.
- `latex-rust 1.0.2` computes a non-zero-width accent shift with `max(base_height,
  AccentBaseHeight)`. The resulting overlay box retains that inflated height, so a following nested
  accent sees an already over-raised base and repeats the error.
- OpenType `FlattenedAccentBaseHeight` controls the optional `flac` glyph substitution; it is not a
  replacement for `AccentBaseHeight` in LuaTeX's vertical-placement formula.

latex-rust-fixes adaptation:
- Repair only direct AST chains composed of `hat`, `widehat`, `tilde` and `widetilde`; a lone accent
  remains on the previously audited rendering path.
- Traverse the chain bottom-up. For each layer, recover the exact accent glyph scale from the typed
  box, select the same STIX horizontal variant as the renderer, and set wrapper height/depth from
  `max(base_height - AccentBaseHeight, 0)` plus the selected accent glyph metrics.
- Recognize only the exact `latex-rust` accent overlap topology, with an optional leading-kern HList
  introduced by its horizontal `shift_x` helper. Any other topology is left upstream rather than
  guessed from box shape.
- No LuaLaTeX stress-case dimensions or empirical offsets are encoded in production code.

Crate targets:
- `src/accents.rs`

Verification:
- `semantic_nested_hat_tilde_chain_propagates_repaired_inner_height` proves that corrected inner
  accent geometry reaches the outer layer instead of retaining the upstream compounded height.
- `semantic_single_hat_tilde_is_not_claimed_by_nested_accent_repair` proves that existing single
  hat/tilde behavior remains outside this narrowly scoped compatibility repair.
- Stress-oracle case `hard-accent-nested` independently compares the complete stack against
  LuaLaTeX + unicode-math.

Sources reviewed:
- https://github.com/TeX-Live/texlive-source/blob/6f36c3f6f194e011f3d08ab6be5e385af79656b8/texk/web2c/luatexdir/tex/mlist.c
- https://learn.microsoft.com/typography/opentype/spec/math
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs

## P-LATEX-INTEGRAL-SCRIPTS-001

Kind: OpenType/LuaTeX no-limits integral script geometry repair for `latex-rust 1.0.2`; no source copied.

External sources:
- LuaTeX `mlist.c` `make_op`, `make_scripts` and `check_nucleus_complexity` implementations.
- OpenType MATH italic-correction and script-placement definitions.
- `latex-rust 1.0.2` `Engine::large_op` and `Engine::attach_scripts_to_box` implementations.

Relevant facts:
- Display integrals select an enlarged operator glyph but retain side scripts (`\\nolimits`) rather than
  the above/below limits used by display sums and products.
- LuaTeX centers the enlarged operator nucleus on the MATH axis before attaching scripts. Once that
  nucleus is boxed, script baselines are constrained by `SuperscriptBaselineDropMax` and
  `SubscriptBaselineDropMin` in addition to the ordinary superscript/subscript constraints.
- For an OpenType no-limits operator, the MATH italic correction participates in horizontal script
  anchoring instead of becoming one common positive gap before both scripts: the operator width is
  normalized by that correction and the superscript is shifted relative to the subscript.
- `latex-rust 1.0.2` routes every integral through its generic simple-character script attachment.
  It therefore omits the boxed-nucleus baseline-drop constraints and, whenever a superscript is
  present, inserts the full operator italic correction before the common overlap slot.

latex-rust-fixes adaptation:
- Repair only AST-identified scripted integrals in Display style and only while the exact upstream
  script-attachment topology remains recognizable. Unscripted integrals and integral variant
  selection remain untouched.
- Recover the selected integral glyph scale and MATH italic correction from the typed box, center
  the glyph on the current MATH axis, derive baseline-drop constraints directly from the font's
  OpenType MATH constants, then reapply the existing ordinary and paired-script constraints.
- Replace the upstream common positive italic gap with the no-limits geometry: subtract the italic
  correction before the shared script slot and offset only the superscript branch by that amount.
- No LuaLaTeX stress dimensions or integral-specific empirical offsets are encoded in production
  code; all quantities come from the selected glyph, current style and OpenType MATH.

Crate targets:
- `src/operators.rs`

Verification:
- `semantic_display_contour_integral_restores_nolimits_geometry` protects the MATH italic-width
  normalization, boxed baseline-drop constraint and display-axis centering for a subscripted
  contour integral.
- `semantic_row_integral_rebuild_propagates_child_geometry` protects propagation through a direct
  top-level Row, which is the shape used by realistic integral expressions.
- `semantic_unscripted_double_integral_is_not_claimed_by_integral_script_repair` proves that the
  already-convergent unscripted multi-integral path remains untouched.
- Stress-oracle cases `hard-integral-gaussian`, `hard-integral-rational`, `hard-double-integral`
  and `hard-contour-integral` provide independent LuaLaTeX geometry measurements.

Sources reviewed:
- https://github.com/TeX-Live/texlive-source/blob/6f36c3f6f194e011f3d08ab6be5e385af79656b8/texk/web2c/luatexdir/tex/mlist.c
- https://learn.microsoft.com/typography/opentype/spec/math
- https://github.com/jscarr64/LaTeX-Rust/blob/b5391dd306a792a7327a0a76bfa84fb9827d77c5/src/layout/engine.rs
