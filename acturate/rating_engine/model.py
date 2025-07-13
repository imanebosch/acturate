import json
from typing import Dict, List, Union

from .nodes import (
    CategoricalNode,
    FixedNode,
    InputNode,
    Node,
    NumericalNode,
    OperationNode,
)
from .operators import OPERATORS

MIN_RATE = "min"
MAX_RATE = "max"


class Rate:
    def __init__(self, name: str, tree: dict):
        self.name = name
        self.rate = self._build_rate(tree)

    def evaluate(self, data: dict):
        """
        Predicts the rate based on the input data.
        """

        return self.rate.evaluate(data)

    def _build_rate(self, tree: Union[str, dict, float, int]) -> Node:
        """
        Recursively builds a tree of nodes from a nested dictionary structure.

        Args:
            tree (Union[str, dict, float, int]): The input data to build the tree from.
            It can be a string, dictionary, float, or integer.

        Returns:
            Node: The root node of the constructed tree.
        """

        if not isinstance(tree, dict):
            return InputNode(value=tree, type="input")

        node_type = tree["type"]

        if node_type == "operation":
            return OperationNode(
                type=node_type,
                operator=OPERATORS[tree["operator"]],
                first_value=self._build_rate(tree["first_value"]),
                second_value=self._build_rate(tree["second_value"]),
            )
        elif node_type == "fixed":
            return FixedNode(value=tree["value"], type=node_type)
        elif node_type == "categorical":
            return CategoricalNode(
                value=self._build_rate(tree["value"]),
                type=node_type,
                categories=tree["categories"],
                beta=tree["beta"],
            )
        elif node_type == "numerical":
            return NumericalNode(
                value=self._build_rate(tree["value"]),
                type=node_type,
                intervals=tree["intervals"],
                beta=tree["beta"],
            )
        elif node_type == "input":
            return InputNode(value=tree["value"], type=node_type)

        else:
            raise ValueError(f"Unknown node type: {node_type}")


class Coverage:
    MAX_VALUE = 10000

    def __init__(self, name: str):
        self.rates: List[Rate] = []
        self.name = name

    def add_rate(self, rate: Rate):
        self.rates.append(rate)

    def price(self, data: dict):
        """
        Predicts the rate based on the input data.
        """
        value, min_value, max_value = (1, 0, self.MAX_VALUE)
        for rate in self.rates:
            if rate.name == MIN_RATE:
                min_value = rate.evaluate(data)
            elif rate.name == MAX_RATE:
                max_value = rate.evaluate(data)
            else:
                value = rate.evaluate(data) * value

        return round(min(max(min_value or 0, value), max_value or self.MAX_VALUE), 2)


class Model:
    def __init__(self):
        self.coverages: List[Coverage] = []

    def price(self, data: dict):
        """
        Predicts the rate based on the input data.
        """
        result = {}
        for cover in self.coverages:
            result[cover.name] = cover.price(data)

        return result

    def load_model(self, path: str):
        """
        Loads the model from a JSON file.

        Args:
            path (str): The path to the JSON file.
        """

        try:
            with open(path, "r") as f:
                data: Dict[str, Dict[str, dict]] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading model: {e}")

        # Clear existing coverages and attributes
        self.coverages.clear()
        for attr in list(self.__dict__.keys()):
            if isinstance(getattr(self, attr), Coverage):
                delattr(self, attr)

        # Load new coverages
        for coverage_name, rates in data.items():
            cover = Coverage(name=coverage_name)
            for rate_name, rate_data in rates.items():
                cover.add_rate(Rate(name=rate_name, tree=rate_data))

            self.coverages.append(cover)
            setattr(self, coverage_name, cover)
