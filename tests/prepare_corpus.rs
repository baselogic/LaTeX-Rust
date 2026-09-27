use latex_rust::{MathFont, MathStyle, layout, parse};
use std::collections::BTreeSet;

const PREPARE_CORPUS_TSV: &str = include_str!("fixtures/prepare_corpus.tsv");

#[derive(Clone, Copy)]
struct PrepareCase<'a> {
    name: &'a str,
    source: &'a str,
    display: bool,
}

fn parse_prepare_cases(tsv: &str) -> Vec<PrepareCase<'_>> {
    let mut cases = Vec::new();
    let mut names = BTreeSet::new();
    let mut formulas = BTreeSet::new();
    for (line_index, raw) in tsv.lines().enumerate() {
        let line = raw.trim_end_matches('\r');
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let mut fields = line.split('\t');
        let name = fields.next().expect("prepare case name");
        let style = fields.next().expect("prepare case style");
        let source = fields
            .next()
            .unwrap_or_else(|| panic!("missing prepare source at line {}", line_index + 1));
        assert!(
            fields.next().is_none(),
            "unexpected prepare field at line {}",
            line_index + 1
        );
        assert!(
            name.bytes()
                .all(|b| b.is_ascii_alphanumeric() || matches!(b, b'-' | b'_')),
            "unsupported prepare case name at line {}",
            line_index + 1
        );
        assert!(
            !name.is_empty() && !source.is_empty(),
            "empty prepare field at line {}",
            line_index + 1
        );
        let display = match style {
            "text" => false,
            "display" => true,
            _ => panic!("invalid prepare style at line {}", line_index + 1),
        };
        assert!(
            names.insert(name),
            "duplicate prepare case name '{name}' at line {}",
            line_index + 1
        );
        assert!(
            formulas.insert((display, source)),
            "duplicate prepare formula at line {}",
            line_index + 1
        );
        cases.push(PrepareCase {
            name,
            source,
            display,
        });
    }
    cases
}

#[test]
fn prepare_corpus_fixture_is_well_formed() {
    let cases = parse_prepare_cases(PREPARE_CORPUS_TSV);
    assert_eq!(cases.len(), 158);
    assert_eq!(cases.iter().filter(|case| !case.display).count(), 26);
    assert_eq!(cases.iter().filter(|case| case.display).count(), 132);
}

#[test]
fn prepare_corpus_composes_every_case() {
    let cases = parse_prepare_cases(PREPARE_CORPUS_TSV);
    let font = MathFont::stix_two_math().expect("STIX Two Math");
    let mut failures = Vec::new();
    for case in cases {
        let style = if case.display {
            MathStyle::Display
        } else {
            MathStyle::Text
        };
        let error = match parse(case.source) {
            Ok(ast) => layout(&ast, &font, style)
                .err()
                .map(|error| format!("layout: {error}")),
            Err(error) => Some(format!("parse: {error}")),
        };
        if let Some(error) = error {
            failures.push(format!(
                "case={} display={} error={error}\nsource={}",
                case.name, case.display, case.source
            ));
        }
    }
    assert!(
        failures.is_empty(),
        "prepare corpus failures:\n{}",
        failures.join("\n\n")
    );
}
