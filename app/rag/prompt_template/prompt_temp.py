from langchain_core.prompts import ChatPromptTemplate


def prompt_temp(PROMPT: str) -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                PROMPT,
            ),
            ("human", "{question}"),
        ]
    )

    return prompt
