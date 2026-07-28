from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

def get_llm():
    return ChatGoogleGenerativeAI(
        model = "gemini-3.5-flash",
        temperature = 0
    )