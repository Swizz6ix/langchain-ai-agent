from typing import Any

from langchain_core.documents import Document


def split_handbook(handbook: Any) -> list[Document]:
    handbook_docs = []

    for page_num, page in enumerate(handbook.pages):
        text = page.extract_text() or ""

        if text.strip():
            handbook_docs.append(
                Document(page_content=text, metadata={"source": "handbook", "page": page_num})
            )

    return handbook_docs
