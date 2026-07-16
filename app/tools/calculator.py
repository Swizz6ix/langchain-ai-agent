from typing import Any


def calculator(expression: str) -> (Any | None):
    """
    Evaluates a mathematical expression and returns the result.

    Args:
        expression (str): A string containing a mathematical expression.
    Returns:
        float: The result of evaluating the mathematical expression.
    """
    # This line of code is for testing purposes
    # raise ConnectionError("Service API Unavailable")
    try:
        #     """
        # NOTE:
        #     Using eval() only for demonstration.
        #     Never use eval() on untrusted user input.

        #     This is because eval() can execute arbitrary code such as `os.system('rm -rf /')`,
        #     which can lead to security vulnerabilities.
        #     In a production environment, consider using a safe math expression parser or library.
        #     """
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None
