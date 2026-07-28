import re
from typing import Any

from langchain_core.documents import Document


def split_faq(faq: Any) -> list[Document]:
    faq_docs = []
    
    for page_num, page in enumerate(faq.pages):
        text = page.extract_text() or ""

        for i, section in enumerate(re.split(r"(?=Q\.)", text)):
            if section.strip():
                faq_docs.append(
                    Document(
                        page_content=section.strip(),
                        metadata={
                            "source": "faq", 
                            "page": page_num, 
                            "section": i
                        },
                    )
                )

    return faq_docs
