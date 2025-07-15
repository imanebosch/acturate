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

    @pytest.fixture
    def cw93bdda_data(self):
        """Load CW93BDDA test data as a dictionary."""
        data_path = Path(__file__).parent / "rating_engine" / "data" / "CW93BDDA.json"
        with open(data_path, "r") as f:
            return json.load(f)

    @pytest.fixture
    def grb4akzek_data(self):
        """Load GRB4AKZEK test data as a dictionary."""
        data_path = Path(__file__).parent / "rating_engine" / "data" / "GRB4AKZEK.json"
        with open(data_path, "r") as f:
            return json.load(f)

    def test_model_with_cw93bdda_data(self, model, cw93bdda_data):
        """Test model pricing with CW93BDDA test data."""

        result = model.price(cw93bdda_data)

        # Validate that we get results for all coverages
        assert "liability" in result
        assert "roadside_assistance" in result
        assert result["liability"] == 207.9
        assert result["roadside_assistance"] == 49.95

        # Validate liability results
        assert model.liability.base.evaluate(cw93bdda_data) == 100
        assert model.liability.min.evaluate(cw93bdda_data) == 150
        assert model.liability.max.evaluate(cw93bdda_data) == 2500
        assert model.liability.driver_age.evaluate(cw93bdda_data) == 1.1
        assert model.liability.vehicle_fuel_type.evaluate(cw93bdda_data) == 1.89
        assert model.liability.price(cw93bdda_data) == 207.9

        # Validate roadside assistance results
        assert model.roadside_assistance.base.evaluate(cw93bdda_data) == 37.0
        assert model.roadside_assistance.vehicle_age.evaluate(cw93bdda_data) == 1.35
        assert model.roadside_assistance.price(cw93bdda_data) == 49.95

    def test_model_with_grb4akzek_data(self, model, grb4akzek_data):
        """Test model pricing with GRB4AKZEK test data."""
        result = model.price(grb4akzek_data)

        # Validate that we get results for all coverages
        assert "liability" in result
        assert "roadside_assistance" in result
        assert result["liability"] == 163.35
        assert result["roadside_assistance"] == 42.55

        # Validate liability results
        assert model.liability.base.evaluate(grb4akzek_data) == 100
        assert model.liability.min.evaluate(grb4akzek_data) == 150
        assert model.liability.max.evaluate(grb4akzek_data) == 2500
        assert model.liability.driver_age.evaluate(grb4akzek_data) == 1.35
        assert model.liability.vehicle_fuel_type.evaluate(grb4akzek_data) == 1.21
        assert model.liability.price(grb4akzek_data) == 163.35

        # Validate roadside assistance results
        assert model.roadside_assistance.base.evaluate(grb4akzek_data) == 37.0
        assert model.roadside_assistance.vehicle_age.evaluate(grb4akzek_data) == 1.15
        assert model.roadside_assistance.price(grb4akzek_data) == 42.55
