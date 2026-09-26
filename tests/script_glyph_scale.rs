use latex_rust::{layout, parse, render_svg, Dim, MathFont, MathParams, MathStyle, SvgOptions};

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
