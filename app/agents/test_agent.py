from app.agents.supervisor_agent import supervisor_agent

# user_query = "What is the weather in Port Harcourt"
# user_query = "simplify 2(8/4)+9"
user_query = "How do I get a discount"
# user_query = (
#     "What is Artificial Intelligent "
#     "summarize the answer for me."
# )

agent = supervisor_agent()

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": user_query,
            }
        ]
    },
)

response = result["messages"][-1]
# print(">>>>>>>>>>>>>", response)
print("response", response.content)

# for kind, item in stream.interleave("messages", "tool_calls"):
#     if kind == "messages":
#         for token in item.text:
#             print(token, end="", flush=True)

#     elif kind == "tool_calls":
#         print("status", item.completed)
#         print(item.completed)
#         if item.completed != False:
#             print(f"\nTool call: {item.tool_name}({item.input})")
#             print(f"Tool result: {item.output}")
