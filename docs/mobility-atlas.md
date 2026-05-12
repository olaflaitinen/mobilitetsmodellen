# Mobility Atlas

## Overview

The interactive mobility atlas visualises municipality-level (kommun-level) rank-rank
slopes across Sweden. Darker shades indicate lower mobility (higher intergenerational
persistence). The atlas supports exploration of geographic heterogeneity (RQ-2).

## Accessibility

The atlas is designed for WCAG 2.2 AA compliance:

- ARIA role and aria-label on the figure container for screen-reader access.
- High-contrast colour palette (minimum 4.5:1 contrast ratio).
- Keyboard navigation support for region selection.
- Tooltip text available via screen reader.

## Implementation

`reporting.atlas.build_atlas()` builds a Plotly bar chart of municipality estimates
(a choropleth map requires geospatial boundary data not committed to this repository).
`reporting.atlas.export_atlas_html()` exports a self-contained HTML file with ARIA
attributes injected.

## Static Snapshot

A static PNG snapshot of the atlas is generated at each release and stored in
`docs/figures/` for the documentation build.

## Tooltip Schema

Each region tooltip shows:
- Region identifier (SCB Kommunkod)
- Rank-rank slope point estimate
- Standard error (or posterior standard deviation after shrinkage)
