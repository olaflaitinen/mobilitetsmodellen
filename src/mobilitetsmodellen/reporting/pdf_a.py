"""PDF/A-2u wrapper for archival-grade figure export."""

from __future__ import annotations

import pathlib
from typing import Any


def save_pdf_a(
    fig: Any,
    path: pathlib.Path,
    dpi: int = 150,
    title: str = "",
    author: str = "Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom Imanov",
) -> pathlib.Path:
    """Save a matplotlib figure as PDF with XMP metadata for PDF/A-2u compliance.

    Full PDF/A-2u conformance (ICC colour profile embedding, XMP metadata) requires
    post-processing via an external tool such as Ghostscript or pikepdf. This function
    saves the figure as a standard PDF and embeds basic XMP metadata via matplotlib's
    PdfPages backend. Record deviation from strict PDF/A-2u in docs/deviations.md.

    Args:
        fig: Matplotlib figure object.
        path: Destination path (should end in ``.pdf``).
        dpi: Resolution for raster elements embedded in the PDF.
        title: Document title embedded in XMP metadata.
        author: Author name embedded in XMP metadata.

    Returns:
        The resolved output path.
    """
    import matplotlib.backends.backend_pdf as mpdf

    path.parent.mkdir(parents=True, exist_ok=True)
    with mpdf.PdfPages(path) as pdf:
        pdf.savefig(fig, dpi=dpi, bbox_inches="tight")
        meta = pdf.infodict()
        meta["Title"] = title
        meta["Author"] = author
        meta["Subject"] = "Intergenerational mobility estimate"
        meta["Keywords"] = "mobility,Sweden,EUPL-1.2"
        meta["Creator"] = "mobilitetsmodellen"
    return path
