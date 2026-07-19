from app.tools.calculator import calculator
from app.tools.get_weather import get_weather
from app.tools.web_search import web_search
from app.tools.text_summarizer import text_summarizer

from app.llm.provider import get_llm
from langchain.agents import create_agent

from app.prompts.system import SYSTEM_PROMPT


tools = [
    calculator,
    get_weather,
    web_search,
    text_summarizer
]

agent = create_agent(
    model=get_llm(),
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)