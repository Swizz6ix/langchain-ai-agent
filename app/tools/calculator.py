from typing import Any

from langchain.tools import tool
from simpleeval import simple_eval


@tool
def calculator(expression: str) -> Any | None:
    """
    Evaluates a mathematical expression and returns the result.

    Args:
        expression (str): A string containing a mathematical expression.
    Returns:
        float: The result of evaluating the mathematical expression.
    """

    try:
        return simple_eval(expression)

    except Exception:
        return None
