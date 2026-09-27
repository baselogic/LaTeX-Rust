#!/usr/bin/env python3
"""Differential LaTeX-Rust math-layout oracle against LuaLaTeX + unicode-math."""
from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
CASE_RE = re.compile(
    r"^LATEX_RUST_MATH_COMPARE case=(?P<case>[A-Za-z0-9_-]+) "
    r"family=(?P<family>[A-Za-z0-9_-]+(?:,[A-Za-z0-9_-]+)*) "
    r"aliases=(?P<aliases>[A-Za-z0-9_-]+(?:,[A-Za-z0-9_-]+)*) "
    r"style=(?P<style>text|display) size_pt=(?P<size>[0-9]+) "
    r"source_utf8_hex=(?P<hex>[0-9a-fA-F]+) width_em=(?P<width>[0-9.]+) "
    r"ascent_em=(?P<ascent>[0-9.]+) descent_em=(?P<descent>[0-9.]+) "
    r"glyphs=(?P<glyphs>[0-9]+) rules=(?P<rules>[0-9]+) ops=(?P<ops>[0-9]+)$"
)
PARAMS_RE = re.compile(
    r"^LATEX_RUST_MATH_COMPARE_PARAMS script_percent=(\d+) scriptscript_percent=(\d+)$"
)
CENSUS_RE = re.compile(
    r"^LATEX_RUST_MATH_COMPARE_CASES names=([A-Za-z0-9_-]+(?:,[A-Za-z0-9_-]+)*)$"
)


class OracleError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise OracleError(message)


def parse_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise OracleError(f"invalid float: {value}") from error
    if not math.isfinite(parsed):
        fail(f"non-finite float: {value}")
    return parsed


def parse_int(value: str, what: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise OracleError(f"invalid {what}: {value}") from error
    if parsed < 0:
        fail(f"negative {what}: {value}")
    return parsed


def utf8hex(value: str) -> str:
    try:
        return bytes.fromhex(value).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as error:
        raise OracleError("invalid UTF-8 fixture hex") from error


def parse_probe(lines: Iterable[str], stress: bool) -> tuple[dict[str, dict], int, int]:
    cases: dict[str, dict] = {}
    expected: list[str] | None = None
    aliases: set[str] = set()
    script = scriptscript = None
    for raw in lines:
        line = raw.rstrip("\r\n")
        match = CENSUS_RE.match(line)
        if match:
            if expected is not None:
                fail("duplicate math case census")
            expected = match.group(1).split(",")
            continue
        match = PARAMS_RE.match(line)
        if match:
            if script is not None:
                fail("duplicate math parameter line")
            script, scriptscript = map(int, match.groups())
            continue
        match = CASE_RE.match(line)
        if not match:
            if line.startswith("LATEX_RUST_MATH_COMPARE"):
                fail(f"malformed math probe record: {line}")
            continue
        fields = match.groupdict()
        name = fields["case"]
        if name in cases:
            fail(f"duplicate math case: {name}")
        case_aliases = fields["aliases"].split(",")
        if case_aliases[0] != name:
            fail(f"noncanonical case alias: {name}")
        if any(alias in aliases for alias in case_aliases):
            fail(f"duplicate case alias: {name}")
        aliases.update(case_aliases)
        size = int(fields["size"])
        if not 1 <= size <= 4096:
            fail(f"invalid case size: {size}")
        cases[name] = {
            "name": name,
            "family": fields["family"],
            "aliases": case_aliases,
            "style": fields["style"],
            "size": size,
            "source": utf8hex(fields["hex"]),
            "width": parse_float(fields["width"]),
            "ascent": parse_float(fields["ascent"]),
            "descent": parse_float(fields["descent"]),
            "glyphs": int(fields["glyphs"]),
            "rules": int(fields["rules"]),
            "ops": int(fields["ops"]),
        }
    if expected is None or set(expected) != set(cases) or len(expected) != len(cases):
        fail("math probe case census missing/incomplete")
    expected_cases, expected_aliases = (89, 94) if stress else (21, 21)
    if len(cases) != expected_cases or len(aliases) != expected_aliases:
        fail(
            f"math profile census changed: {len(cases)} measurements, {len(aliases)} aliases"
        )
    if script is None or scriptscript is None or not (0 < scriptscript <= script <= 100):
        fail("invalid/missing embedded font script parameters")
    return cases, script, scriptscript


def build_tex(
    cases: dict[str, dict], result: str, script: int, scriptscript: int, font_name: str
) -> str:
    out = [
        r"\documentclass{article}",
        r"\usepackage{unicode-math}",
        rf"\setmathfont{{{font_name}}}[Path=./]",
    ]
    for size in sorted({case["size"] for case in cases.values()}):
        out.append(
            rf"\DeclareMathSizes{{{size}}}{{{size}}}{{{size * script / 100:.6f}}}"
            rf"{{{size * scriptscript / 100:.6f}}}"
        )
    out += [
        r"\pagestyle{empty}",
        r"\mathsurround=0pt",
        rf"\directlua{{latex_rust_math_result_file='{result}'; dofile('math_compare.lua')}}",
        r"\begin{document}",
    ]
    for case in cases.values():
        if re.search(r"[\r\n%]", case["source"]) or not re.fullmatch(
            r"[A-Za-z0-9_-]+", case["name"]
        ):
            fail(f"unsafe math fixture: {case['name']}")
        style = r"\displaystyle" if case["style"] == "display" else r"\textstyle"
        size = case["size"]
        out += [
            r"\begingroup",
            rf"\fontsize{{{size}pt}}{{{size}pt}}\selectfont",
            rf"\setbox0=\hbox{{$" + style + " " + case["source"] + "$}",
            r"\setbox2=\hbox{$\textstyle x$}",
            r"\dimen0=1em",
            rf"\directlua{{latex_rust_measure_math_case('{case['name']}', 0, 2, tex.dimen[0])}}",
            r"\endgroup",
        ]
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def parse_results(path: Path, cases: dict[str, dict]) -> dict[str, dict]:
    if not path.is_file():
        fail(f"LuaLaTeX did not produce {path.name}")
    result: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("|")
        if len(parts) != 12 or parts[0] != "CASE" or parts[1] not in cases:
            fail(f"unexpected/malformed LuaTeX math result: {line}")
        name = parts[1]
        if name in result:
            fail(f"duplicate LuaTeX math case: {name}")
        text_em, math_em = parse_float(parts[5]), parse_float(parts[11])
        if text_em <= 0 or math_em <= 0:
            fail(f"non-positive text/math em: {name}")
        if abs(math_em - cases[name]["size"] * 65536) > 2:
            fail(f"LuaTeX selected wrong math size for {name}")
        result[name] = {
            "width": parse_float(parts[2]) / math_em,
            "ascent": parse_float(parts[3]) / math_em,
            "descent": parse_float(parts[4]) / math_em,
            "text_em": text_em,
            "glyphs": parse_int(parts[6], "glyph count"),
            "rules": parse_int(parts[7], "rule count"),
            "hlists": parse_int(parts[8], "hlist count"),
            "vlists": parse_int(parts[9], "vlist count"),
            "max_depth": parse_int(parts[10], "max depth"),
            "math_em": math_em,
        }
    if len(result) != len(cases):
        fail(f"expected {len(cases)} LuaTeX cases, got {len(result)}")
    return result


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> list[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    process = subprocess.run(
        command,
        cwd=cwd,
        env=merged,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    lines = process.stdout.splitlines()
    if process.returncode != 0:
        tail = "\n".join(lines[-80:])
        fail(f"command failed ({process.returncode}): {' '.join(command)}\n{tail}")
    return lines


def percentile_nearest_rank(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(percentile / 100 * len(ordered)) - 1))
    return ordered[index]


def run_oracle(*, stress: bool, tolerance: float, top_worst: int, diagnostic: bool) -> None:
    if not math.isfinite(tolerance) or tolerance < 0:
        fail("tolerance must be finite and non-negative")
    if top_worst < 1:
        fail("top-worst must be positive")
    lua_source = ROOT / "tools" / "math_compare.lua"
    if not lua_source.is_file():
        fail("tools/math_compare.lua is missing")

    with tempfile.TemporaryDirectory(prefix="latex-rust-math-") as tmp:
        work = Path(tmp)
        shutil.copy2(lua_source, work / "math_compare.lua")
        font = work / "STIXTwoMath-LaTeXRust.otf"
        env = {"LATEX_RUST_MATH_COMPARE_FONT_PATH": str(font)}
        if stress:
            env["LATEX_RUST_MATH_COMPARE_STRESS"] = "1"
        lines = run(
            [
                "cargo",
                "test",
                "--manifest-path",
                str(ROOT / "Cargo.toml"),
                "--test",
                "math_oracle",
                "--release",
                "lualatex_math_comparison_probe",
                "--",
                "--exact",
                "--ignored",
                "--nocapture",
            ],
            cwd=ROOT,
            env=env,
        )
        cases, script, scriptscript = parse_probe(lines, stress)
        if not font.is_file():
            fail("Rust probe did not export the embedded math font")
        tex = work / "math-compare.tex"
        result = work / "math-compare.tsv"
        tex.write_text(
            build_tex(cases, result.name, script, scriptscript, font.name), encoding="utf-8"
        )
        run(
            [
                "lualatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                tex.name,
            ],
            cwd=work,
        )
        reference = parse_results(result, cases)

        deltas: list[tuple[float, str, str, int]] = []
        divergent: list[str] = []
        structural: list[str] = []
        for case in cases.values():
            ref = reference[case["name"]]
            delta = max(
                abs(case["width"] - ref["width"]),
                abs(case["ascent"] - ref["ascent"]),
                abs(case["descent"] - ref["descent"]),
            )
            deltas.append((delta, case["name"], case["family"], case["size"]))
            if delta > tolerance:
                divergent.append(case["name"])
            if case["glyphs"] != ref["glyphs"] or case["rules"] != ref["rules"]:
                structural.append(case["name"])

        values = [item[0] for item in deltas]
        maximum = max(values) if values else 0.0
        print(
            f"{len(cases) - len(divergent)}/{len(cases)} <= {tolerance:.3f}em; "
            f"p95={percentile_nearest_rank(values, 95):.6f}; max={maximum:.6f}; "
            f"structural={len(structural)}"
        )
        if stress or divergent:
            for delta, name, family, size in sorted(deltas, reverse=True)[:top_worst]:
                print(f"{name}\t{family}\t{size}pt\t{delta:.6f}em")
        if structural:
            print("structure mismatches: " + ", ".join(structural))
        if divergent and not diagnostic:
            fail(f"math comparison exceeded {tolerance}em: {', '.join(divergent)}")


def self_test() -> None:
    names = [f"case-{index}" for index in range(1, 22)]
    params = "LATEX_RUST_MATH_COMPARE_PARAMS script_percent=70 scriptscript_percent=50"
    census = "LATEX_RUST_MATH_COMPARE_CASES names=" + ",".join(names)
    rows = [
        "LATEX_RUST_MATH_COMPARE "
        f"case={name} family=basic aliases={name} style=text size_pt=10 source_utf8_hex=78 "
        "width_em=1.0 ascent_em=0.5 descent_em=0.0 glyphs=1 rules=0 ops=1"
        for name in names
    ]
    cases, script, scriptscript = parse_probe([params, census, *rows], False)
    assert len(cases) == 21 and script == 70 and scriptscript == 50
    tex = build_tex(cases, "result.tsv", script, scriptscript, "STIXTwoMath.otf")
    assert "latex_rust_measure_math_case" in tex


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stress", action="store_true")
    parser.add_argument("--tolerance", type=float, default=0.05)
    parser.add_argument("--top-worst", type=int, default=25)
    parser.add_argument("--diagnostic", action="store_true", help="report deltas without failing")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
        else:
            run_oracle(
                stress=args.stress,
                tolerance=args.tolerance,
                top_worst=args.top_worst,
                diagnostic=args.diagnostic,
            )
    except OracleError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
