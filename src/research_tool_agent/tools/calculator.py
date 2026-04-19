from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Useful for evaluating simple mathematical expressions.
    Input should be a valid Python math expression (e.g., '12 * (4 + 3) / 2').
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of '{expression}' is {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"