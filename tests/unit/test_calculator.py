from app.tools.calculator import calculator


def test_calculator_addition() -> None:
    result = calculator.invoke({"expression": "10 + 5"})

    assert result == 15


def test_calculator_invalid_expression() -> None:
    result = calculator.invoke({"expression": "hello + world"})

    assert result is None
