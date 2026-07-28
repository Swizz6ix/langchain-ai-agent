from langchain_core.prompts import ChatPromptTemplate

def prompt_temp(PROMPT):
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            PROMPT,
        ),
        (
            "human",
            "{question}"
        )
    ])

    return prompt