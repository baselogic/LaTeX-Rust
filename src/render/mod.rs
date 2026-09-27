//! Render backends: SVG, PNG (`tiny-skia`, feature `png`), and egui
//! (`features = ["egui"]`).
//!
//! Pipeline: [`crate::layout::MathBox`] → this module. SVG is the v1 output.
//! PNG and egui are optional. Without their features those entry points return
//! [`crate::Error::Unsupported`].

pub mod egui;
pub mod png;
pub mod svg;

use core::cmp::Ordering;

use crate::dim::Dim;
use crate::error::Error;
use crate::font::MathFont;
use crate::layout::{BoxContent, MathBox};

#[cfg(feature = "egui")]
pub use egui::{latex_to_shapes, paint_egui, shapes};
pub use egui::{render_egui, EguiOptions};
pub use png::{latex_to_png, render_png, PngBackground, PngOptions};
pub use svg::{latex_to_svg, render_svg, SvgOptions};

/// Recover the outline scale already encoded in a glyph box's exact layout metrics.
///
/// LR-SCRIPT-GLYPH-SCALE-010: layout scales Script/ScriptScript glyph metrics, while the
/// renderer starts from the font's unscaled outline coordinates. External renderers must use
/// this function rather than reconstructing that scale from private layout assumptions.
///
/// # Errors
///
/// Returns [`Error::Malformed`] when `bx` is not a glyph box, its encoded metrics imply an
/// inconsistent or non-positive scale, or no non-zero metric can establish a scale. Font lookup
/// failures are propagated unchanged.
pub fn glyph_render_scale(bx: &MathBox, font: &MathFont) -> Result<Dim, Error> {
    let BoxContent::Glyph { ch, glyph_id } = &bx.content else {
        return Err(Error::Malformed {
            what: "glyph render scale requested for non-glyph box".into(),
        });
    };
    let metrics = font.glyph_id(*ch, *glyph_id)?;
    let mut scale: Option<Dim> = None;

    for (actual, unscaled) in [
        (&bx.width, &metrics.advance),
        (&bx.height, &metrics.height),
        (&bx.depth, &metrics.depth),
    ] {
        if unscaled.is_zero() {
            continue;
        }

        let ratio = actual / unscaled;
        if ratio.cmp(&Dim::zero()) != Some(Ordering::Greater) {
            return Err(Error::Malformed {
                what: "non-positive math glyph render scale".into(),
            });
        }

        if let Some(expected) = &scale {
            if !ratio.eq_dim(expected) {
                return Err(Error::Malformed {
                    what: "inconsistent math glyph render scale".into(),
                });
            }
        } else {
            scale = Some(ratio);
        }
    }

    scale.ok_or_else(|| Error::Malformed {
        what: "math glyph has no metric from which to recover render scale".into(),
    })
}
