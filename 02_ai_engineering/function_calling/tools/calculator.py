from simpleeval import InvalidExpression, SimpleEval


def calculate(expression: str) -> str:
    # Create a safe evaluator
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
        # Catch any other evaluation errors (syntax, unknown functions, etc.)
        return f"Error: {e}"


if __name__ == "__main__":
    print(calculate("2+2"))  # 4
    print(calculate("10/3"))  # 3.3333333333333335
    print(calculate("2**10"))  # 1024
    print(calculate("sqrt(16)"))  # 4.0 (sqrt is available by default)
    print(calculate("10/0"))  # Error: Division by zero
    print(calculate("2+"))  # Invalid expression: unexpected EOF...
    print(
        calculate("__import__('os').system('ls')")
    )  # Error: 'os' is not defined (safe!)
