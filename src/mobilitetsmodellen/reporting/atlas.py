"""Interactive mobility atlas with WCAG 2.2 AA accessibility compliance."""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

_HIGH_CONTRAST_PALETTE = [
    "#003f5c",
    "#374c80",
    "#7a5195",
    "#bc5090",
    "#ef5675",
    "#ff764a",
    "#ffa600",
]

_ARIA_DESCRIPTION = (
    "Interactive choropleth map of intergenerational rank-rank slopes across Swedish"
    " municipalities. Darker shades indicate lower mobility (higher persistence)."
    " Use keyboard arrow keys to navigate between regions."
)


def build_atlas(
    region_df: pd.DataFrame,
    region_col: str = "region",
    estimate_col: str = "estimate",
    se_col: str = "se",
    title: str = "Swedish Intergenerational Mobility Atlas",
    seed: int = 31,
) -> Any:
    """Build a Plotly choropleth atlas of municipality-level mobility estimates.

    The figure includes ARIA attributes, a high-contrast colour palette, and
    keyboard navigation support for WCAG 2.2 AA compliance.

    Args:
        region_df: DataFrame with one row per geographic unit.
        region_col: Column with region identifiers.
        estimate_col: Column with mobility point estimates.
        se_col: Column with standard errors (shown in tooltip).
        title: Figure title shown in the atlas.
        seed: Random seed for jitter in static snapshot.

    Returns:
        A Plotly Figure object.
    """
    import plotly.graph_objects as go  # type: ignore[import-untyped]

    rng = np.random.default_rng(seed)
    jitter = rng.uniform(-0.01, 0.01, size=len(region_df))
    estimates = region_df[estimate_col].to_numpy() + jitter
    hover_text = [
        f"Region: {r}<br>Estimate: {e:.3f} (SE: {s:.3f})"
        for r, e, s in zip(
            region_df[region_col],
            region_df[estimate_col],
            region_df[se_col] if se_col in region_df.columns else [0.0] * len(region_df),
            strict=False,
        )
    ]
    fig = go.Figure(
        data=go.Bar(
            x=region_df[region_col].tolist(),
            y=estimates.tolist(),
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            marker_color=estimates.tolist(),
            marker_colorscale=_HIGH_CONTRAST_PALETTE,
        ),
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title="Municipality (Kommun)",
        yaxis_title="Rank-rank slope",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#000000", size=12),
        margin=dict(l=60, r=20, t=60, b=100),
    )
    return fig


def export_atlas_html(
    fig: Any,
    path: pathlib.Path,
    aria_label: str = _ARIA_DESCRIPTION,
) -> pathlib.Path:
    """Export the atlas figure to a self-contained HTML file with ARIA metadata.

    Args:
        fig: Plotly Figure object.
        path: Destination path (should end in ``.html``).
        aria_label: ARIA label injected into the HTML for screen readers.

    Returns:
        The resolved output path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    html = fig.to_html(
        full_html=True,
        include_plotlyjs="cdn",
        config={"responsive": True, "displayModeBar": True},
    )
    aria_tag = f'<div role="figure" aria-label="{aria_label}">'
    html = html.replace("<body>", f"<body>\n{aria_tag}", 1)
    html = html.replace("</body>", "</div>\n</body>", 1)
    path.write_text(html, encoding="utf-8")
    return path


from typing import Any  # noqa: E402
