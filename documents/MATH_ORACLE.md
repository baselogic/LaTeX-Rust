# LuaLaTeX differential math oracle

The LuaLaTeX oracle is development evidence for LaTeX-Rust layout. It is not a production dependency and it does not participate in parsing, layout, or rendering at runtime.

The Rust probe in `tests/math_oracle.rs` measures the `MathBox` returned by `parse` plus `layout_with_em_size_pt` against the exact embedded STIX Two Math face. The Lua side in `tools/math_compare.lua` measures final LuaTeX math-box width, height, and depth before PDF rasterization. Both sides normalize geometry by the selected root math em.

The ordinary profile contains 21 measurements. `tests/fixtures/math_compare_stress.tsv` adds a bounded 73-case stress corpus; after aliases are deduplicated the combined profile contains 89 unique measurements and 94 case identities. The stress corpus also sweeps selected formulas at 6, 10, 20, and 40 TeX points so absolute TeX dimensions cannot accidentally agree at one physical size.

The oracle exports `ScriptPercentScaleDown` and `ScriptScriptPercentScaleDown` from the embedded font's MATH constants and emits explicit `\DeclareMathSizes` declarations for every requested physical size. LuaLaTeX independently measures a one-glyph control box at each selected size and rejects the run when the root math em does not match the requested size within two scaled points. This prevents a size-selection mismatch from being misreported as a layout defect.

Width, ascent, and descent are the cross-engine geometry observables. Glyph and rule counts are diagnostic only because LuaTeX's internal hlist/vlist decomposition does not need to match LaTeX-Rust's typed box tree. The default divergence threshold is `0.05 em`.

Run the baseline gate with:

```text
python tools/math_oracle.py
```

Run the larger profile diagnostically with:

```text
python tools/math_oracle.py --stress --diagnostic
```

`tools/math_oracle.py` uses temporary files only. It exports the exact embedded font bytes, generates one temporary LuaLaTeX document, parses machine-readable Lua results, and removes the temporary directory after the comparison.

Primary external references:

- LuaTeX reference manual: https://www.luatex.org/svn/trunk/manual/luatex.pdf
- `unicode-math`: https://ctan.org/pkg/unicode-math
- OpenType MATH: https://learn.microsoft.com/en-us/typography/opentype/spec/math
