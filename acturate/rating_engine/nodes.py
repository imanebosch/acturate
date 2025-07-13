from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from .operators import Operator
from .utils import is_in_interval

DEFAULT_ENUM: str = "!default!"


class Node(ABC):
    def __init__(self, type: str) -> None:
        self.type = type

    @abstractmethod
    def evaluate(self, data: Optional[Dict[str, Any]] = None) -> Any:
        pass


class FixedNode(Node):
    def __init__(self, type: str, value: Union[str, float]) -> None:
        self.value = value
        self.type = type

    def evaluate(self, data: Optional[Dict[str, Any]] = None) -> Union[str, float]:
        return self.value


class CategoricalNode(Node):
    def __init__(
        self,
        value: Node,
        type: str,
        categories: List[str],
        beta: List[float],
    ):
        self.value = value
        self.type = type
        self.categories = categories
        self.beta = beta

    def evaluate(self, data: dict = None):
        value = self.value.evaluate(data=data)

        if value is None:
            return self.beta[self.categories.index(None)]

        if str(value) not in self.categories:
            return self.beta[self.categories.index(DEFAULT_ENUM)]
        return self.beta[self.categories.index(str(value))]


class NumericalNode:
    def __init__(self, value: Node, type: str, intervals: List[str], beta: List[float]):
        self.value = value
        self.type = type
        self.beta = beta
        self.intervals = intervals

    def evaluate(self, data: dict = None):
        value = self.value.evaluate(data=data)

        if value is None:
            return self.beta[self.intervals.index(None)]

        for i, interval in enumerate(self.intervals):
            if interval in [DEFAULT_ENUM, None]:
                continue
            if is_in_interval(value, interval):
                return self.beta[i]

        return self.beta[self.intervals.index(DEFAULT_ENUM)]


class InputNode:
    def __init__(self, value: Node, type: str):
        self.value = value
        self.type = type

    def evaluate(self, data: dict = None):
        try:
            return data[self.value]
        except KeyError:
            raise KeyError(f"Key '{self.value}' not found in input data")


class OperationNode:
    def __init__(
        self, type: str, operator: Operator, first_value: Node, second_value: Node
    ):
        self.type = type
        self.operator = operator
        self.first_value = first_value
        self.second_value = second_value

    def evaluate(self, data: dict = None):
        return self.operator.evaluate(
            self.first_value.evaluate(data=data), self.second_value.evaluate(data=data)
        )
