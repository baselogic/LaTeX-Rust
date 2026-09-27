use latex_rust::render::glyph_render_scale;
use latex_rust::{
    BoxContent, Dim, MathBox, MathFont, MathParams, MathStyle, SvgOptions, layout, parse, render_svg,
};

#[test]
fn svg_scales_glyph_outlines_to_the_layout_math_style() {
    let font = MathFont::stix_two_math().expect("STIX Two Math");
    let params = MathParams::from_font(&font).expect("MATH constants");
    let ast = parse("2").expect("digit");
    let options = SvgOptions::new();
    let root_font_unit = &options.font_size_pt / &Dim::from_i64(i64::from(font.units_per_em()));

    for style in [MathStyle::Text, MathStyle::Script, MathStyle::ScriptScript] {
        let tree = layout(&ast, &font, style).expect("layout");
        let svg = render_svg(&tree, &font, &options).expect("svg");
        let expected_font_unit = &root_font_unit * &params.scale(style);
        let expected_transform = format!(
            "scale({} {})",
            expected_font_unit.to_svg_string(),
            (-expected_font_unit).to_svg_string()
        );

        assert!(
            svg.contains(&expected_transform),
            "{style:?} glyph outline did not use layout scale {expected_transform}"
        );
    }
}

fn first_glyph(bx: &MathBox) -> Option<&MathBox> {
    match &bx.content {
        BoxContent::Glyph { .. } => Some(bx),
        BoxContent::HList(children) | BoxContent::VList(children) | BoxContent::Overlap(children) => {
            children.iter().find_map(first_glyph)
        }
        BoxContent::Color(_, inner)
        | BoxContent::BackColor(_, inner)
        | BoxContent::Frame { inner, .. } => first_glyph(inner),
        BoxContent::Empty | BoxContent::Rule | BoxContent::Kern(_) | BoxContent::Line { .. } => None,
    }
}

#[test]
fn public_glyph_render_scale_matches_layout_style_and_rejects_non_glyph_boxes() {
    let font = MathFont::stix_two_math().expect("STIX Two Math");
    let params = MathParams::from_font(&font).expect("MATH constants");
    let ast = parse("2").expect("digit");

    for style in [MathStyle::Text, MathStyle::Script, MathStyle::ScriptScript] {
        let tree = layout(&ast, &font, style).expect("layout");
        let glyph = first_glyph(&tree).expect("layout must contain the digit glyph");
        let scale = glyph_render_scale(glyph, &font).expect("glyph render scale");
        assert!(
            scale.eq_dim(&params.scale(style)),
            "{style:?} public glyph scale must match layout style"
        );
    }

    let err = glyph_render_scale(&MathBox::empty(), &font).expect_err("non-glyph must fail");
    assert!(err.to_string().contains("non-glyph"));
}
