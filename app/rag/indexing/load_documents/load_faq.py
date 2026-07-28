from pathlib import Path
from typing import Any

from pypdf import PdfReader


def load_faq() -> Any:
    faq_path = Path(
        "app/assets/main_frequently-asked-questions-about-your-gm-supplier-discount.pdf"
    )

    if not faq_path.exists():
        raise FileNotFoundError(f"FAQ PDF not found: {faq_path.resolve()}")

    faq = PdfReader(faq_path)

    return faq
