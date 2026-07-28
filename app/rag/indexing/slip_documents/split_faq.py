import re
from langchain_core.documents import Document

def split_faq(faq):
    pages = [
    {
        "page": page_num,
        "text": page.extract_text() or ""
    }

    for page_num, page in enumerate(faq.pages)
    ]

    faq_docs = [
        Document(
            page_content=section.strip(),
            metadata={
                "source": "faq",
                "page": page["page"],
                "section": i
            }
        )

        for page in pages
        for i, section in enumerate(re.split(r"(?=Q\.)", page["text"]))
        if section.strip()
    ]

    return faq_docs