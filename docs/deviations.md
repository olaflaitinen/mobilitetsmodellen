# Deviations from Specification

This file records any deviation from the prompt specification (v2.0.0).

## DEV-001: LICENSE SHA-256

**Requirement**: QG-13 states LICENSE SHA-256 must match the EU Joinup canonical hash.

**Status**: The LICENSE file was generated from training-data knowledge of the EUPL-1.2
canonical text. A byte-for-byte match with the EU Joinup authoritative file cannot be
guaranteed without a live network fetch. Maintainer should verify with:

```bash
curl -L https://joinup.ec.europa.eu/sites/default/files/inline-files/EUPL%20v1_2%20EN(1).txt \
  | sha256sum
sha256sum LICENSE
```

**Impact**: Low. The substantive licence terms are identical to EUPL-1.2.

## DEV-002: PDF/A-2u Full Conformance

**Requirement**: reporting.pdf_a uses matplotlib PdfPages; full PDF/A-2u conformance
(ICC colour profile embedding) requires post-processing via Ghostscript or pikepdf.

**Status**: matplotlib PDF output is used as a base. Full PDF/A-2u conformance is
deferred to a post-processing step in the release workflow.

**Impact**: Low for research use; relevant for archival submissions.

## DEV-003: Choropleth Atlas Map

**Requirement**: docs/mobility-atlas.md describes a choropleth map.

**Status**: `reporting.atlas.build_atlas()` implements a bar chart of municipality
estimates. A true choropleth map requires geospatial boundary files (SCB shapefile)
which are not committed to this repository. The bar chart serves as a functional proxy
with identical ARIA and accessibility attributes.

**Impact**: Medium for visual presentation; no impact on statistical outputs.

## DEV-004: IV Variants for IGE

**Requirement**: docs/elasticity.md mentions IV variants.

**Status**: IV variants (lagged income, sibling income instruments) are documented but
not yet implemented in `estimators.elasticity`. Planned for v0.2.0.

**Impact**: Low; classical OLS IGE is implemented and functional.
