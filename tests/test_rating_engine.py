import json
from pathlib import Path

import pytest

from acturate.rating_engine.model import Model


class TestModel:
    """Integration tests for the rating engine."""

    # TODO: Add more exhaustive tests for the rating engine, including:
    #   - Edge cases for minimum and maximum values
    #   - Invalid or missing input data
    #   - Complex operations

    @pytest.fixture
    def model(self):
        """Load the default model for testing."""
        model = Model()
        model_path = Path(__file__).parent / "rating_engine" / "models" / "default.json"
        model.load_model(str(model_path))
        return model

    def test_model_with_cw93bdda_data(self, model):
        """Test model pricing with CW93BDDA test data."""
        data_path = Path(__file__).parent / "rating_engine" / "data" / "CW93BDDA.json"
        with open(data_path, 'r') as f:
            data = json.load(f)

        result = model.price(data)

        # Validate that we get results for all coverages
        assert "liability" in result
        assert "roadside_assistance" in result

        # Validate that results are numeric and positive
        for coverage, price in result.items():
            assert isinstance(price, (int, float))
            assert price >= 0

    def test_model_with_grb4akzek_data(self, model):
        """Test model pricing with GRB4AKZEK test data."""
        data_path = Path(__file__).parent / "rating_engine" / "data" / "GRB4AKZEK.json"
        with open(data_path, 'r') as f:
            data = json.load(f)

        result = model.price(data)

        # Validate that we get results for all coverages
        assert "liability" in result
        assert "roadside_assistance" in result

        # Validate that results are numeric and positive
        for coverage, price in result.items():
            assert isinstance(price, (int, float))
            assert price >= 0
