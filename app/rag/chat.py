from dotenv import load_dotenv
load_dotenv()

from app.rag.retrieval.question_answer import answer_question


user_query = "How do I get a discount"

ans = answer_question(user_query)

print("answer>>>", ans )
print("answer>>>", type(ans))
