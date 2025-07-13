from typing import Any, Callable, Dict


def addition(first_value: float, second_value: float) -> float:
    return first_value + second_value


def multiplication(first_value: float, second_value: float) -> float:
    return first_value * second_value


def or_operator(first_value: Any, second_value: Any) -> Any:
    return first_value or second_value


def and_operator(first_value: Any, second_value: Any) -> Any:
    return first_value and second_value


def grater_than_operator(first_value: Any, second_value: Any) -> bool:
    return first_value > second_value


def less_than_operator(first_value: Any, second_value: Any) -> bool:
    return first_value < second_value


def concat_operator(first_value: Any, second_value: Any) -> str:
    return str(first_value) + " - " + str(second_value)


def greater_than_or_equal_operator(first_value: Any, second_value: Any) -> bool:
    return first_value >= second_value


def less_than_or_equal_operator(first_value: Any, second_value: Any) -> bool:
    return first_value <= second_value


def not_equal(first_value: Any, second_value: Any) -> bool:
    return first_value != second_value


def equal(first_value: Any, second_value: Any) -> bool:
    return first_value == second_value


class Operator:
    def __init__(self, name: str, function: Callable[[Any, Any], Any]) -> None:
        self.name: str = name
        self.function: Callable[[Any, Any], Any] = function

    def evaluate(self, first_value: Any, second_value: Any) -> Any:
        return self.function(first_value, second_value)


OPERATORS: Dict[str, Operator] = {
    "+": Operator("addition", addition),
    "*": Operator("multiplication", multiplication),
    "or": Operator("or", or_operator),
    "and": Operator("and", and_operator),
    "concat": Operator("concat", concat_operator),
    "<": Operator("less_than", less_than_operator),
    ">": Operator("grater_than", grater_than_operator),
    ">=": Operator("grater_equal_than", greater_than_or_equal_operator),
    "<=": Operator("less_equal_than", less_than_or_equal_operator),
    "!=": Operator("not_equal", not_equal),
    "==": Operator("not_equal", not_equal),
}
