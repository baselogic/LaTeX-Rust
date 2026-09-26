use latex_rust::{layout, parse, styled_char, BoxContent, MathBox, MathFont, MathStyle, TextStyle};

fn glyph_chars(bx: &MathBox, out: &mut Vec<char>) {
    match &bx.content {
        BoxContent::Glyph { ch, .. } => out.push(*ch),
        BoxContent::HList(children)
        | BoxContent::VList(children)
        | BoxContent::Overlap(children) => {
            for child in children {
                glyph_chars(child, out);
            }
        }
        BoxContent::Color(_, inner)
        | BoxContent::BackColor(_, inner)
        | BoxContent::Frame { inner, .. } => glyph_chars(inner, out),
        BoxContent::Empty | BoxContent::Rule | BoxContent::Kern(_) | BoxContent::Line { .. } => {}
    }
}

fn laid_out_glyphs(source: &str) -> Vec<char> {
    let ast = parse(source).expect("parse default-math-italic case");
    let font = MathFont::stix_two_math().expect("embedded STIX Two Math");
    let bx = layout(&ast, &font, MathStyle::Text).expect("layout default-math-italic case");
    let mut glyphs = Vec::new();
    glyph_chars(&bx, &mut glyphs);
    glyphs
}

#[test]
fn bare_variables_use_default_math_italic_without_overriding_explicit_styles() {
    assert_eq!(laid_out_glyphs("x"), vec![styled_char('x', TextStyle::It)]);
    assert_eq!(
        laid_out_glyphs(r"\alpha"),
        vec![styled_char('α', TextStyle::It)]
    );
    assert_eq!(laid_out_glyphs(r"\mathrm{x}"), vec!['x']);
    assert_eq!(
        laid_out_glyphs(r"\mathbf{x}"),
        vec![styled_char('x', TextStyle::Bf)]
    );
    assert_eq!(laid_out_glyphs("1"), vec!['1']);
}
