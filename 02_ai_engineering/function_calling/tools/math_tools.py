from simpleeval import InvalidExpression, SimpleEval


def calculate(expression: str) -> str:
    evaluator = SimpleEval()
    try:
        result = evaluator.eval(expression)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except InvalidExpression as e:
        return f"Invalid expression: {e}"
    except Exception as e:
        return f"Error: {e}"


def add(a: float, b: float) -> str:
    return str(a + b)


def multiply(a: float, b: float) -> str:
    return str(a * b)


SCHEMAS = [
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression (supports arithmetic and math functions like sqrt, pow)",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate, e.g. '2 + sqrt(16)'"}
            },
            "required": ["expression"],
        },
    },
    {
        "name": "add",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["a", "b"],
        },
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["a", "b"],
        },
    },
]


if __name__ == "__main__":
    print(calculate("2+2"))
    print(calculate("sqrt(16)"))
    print(calculate("10/0"))
    print(add(3, 4))
    print(multiply(6, 7))
