from pathlib import Path
from typing import Any

from pypdf import PdfReader


def load_handbook() -> Any:
    handBook_path = Path("app/assets/Employee-Handbook.pdf")

    if not handBook_path.exists():
        raise FileNotFoundError(f"Handbook PDF not found: {handBook_path.resolve()}")

    handBook = PdfReader(handBook_path)

    return handBook
