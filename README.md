# ActuRate

An actuarial rating engine for insurance pricing.

## Summary

ActuRate is a flexible rating engine that allows you to define complex pricing models using a JSON configuration. It supports various types of rating factors including:

- **Fixed values**: Constant rates or factors
- **Categorical factors**: Discrete categories with associated multipliers
- **Numerical factors**: Continuous ranges with associated multipliers
- **Operations**: Mathematical and logical operations between factors
- **Input values**: Dynamic values from quote data

## Installation

```bash
pip install acturate
```

## Quick Start

### Basic Usage

```python
from acturate.rating_engine.model import Model

# Create a rating model
pricing = Model()

# Load a pricing model from JSON
pricing.load_model("path/to/model.json")

# Price a quote with input data
quote_data = {
    "driver_age": 27,
    "vehicle_age": 10.09,
    "vehicle_fuel_type": "diesel"
}

result = pricing.price(quote_data)
print(result)
# Output: {'liability': 77.02, 'roadside_assistance': 37.0}
```

## Model Configuration

ActuRate models are defined in JSON format with the following structure:

```json
{
  "coverage_name": {
    "base": {
      "type": "fixed",
      "value": 100.0
    },
    "factor_name": {
      "type": "categorical|numerical|operation",
      // ... factor-specific configuration
    },
    "min": {
        "type": "fixed",
        "value": 50.0
    },
    "max": {
        "type": "fixed",
        "value": 500.0
    }
  }
}
```

### Node Types

#### 1. Fixed Node
Constant values that don't change based on input data.

```json
{
  "type": "fixed",
  "value": 100.0
}
```

#### 2. Input Node
References values from the input quote data.

```json
{
  "type": "input",
  "value": "driver_age"
}
```

#### 3. Categorical Node
Applies different multipliers based on discrete categories.

```json
{
  "type": "categorical",
  "value": "vehicle_fuel_type",
  "categories": [null, "!default!", "diesel", "gasoline", "hybrid", "electric"],
  "beta": [1.0, 1.0, 1.0, 1.2, 1.0, 1.2, 1.3]
}
```

**Special categories:**
- `!default!`: When the input value doesn't match any category
- `null`: When the input value is null

#### 4. Numerical Node
Applies different multipliers based on numerical ranges.

```json
{
  "type": "numerical",
  "value": "driver_age",
  "intervals": [null, "!default!", "[18, 25)", "[25, 35)", "[35, 50)", "[50, 65)", "[65, 100]"],
  "beta": [1.5, 1.5, 1.0, 1.8, 1.2, 1.0, 1.1, 1.3]
}
```

**Interval formats:** 
- `[min, max)`: Closed on the left and open oon the right
- `!default!`: Rate the input value is not within any interval
- `null`: Rate when the input value is null

#### 5. Operation Node
Performs mathematical or logical operations between two values.

```json
{
  "type": "operation",
  "operator": "*",
  "first_value": {
    "type": "fixed",
    "value": 1.1
  },
  "second_value": {
    "type": "input",
    "value": "base_rate"
  }
}
```

**Available operators:**
- `+`: Addition
- `*`: Multiplication
- `or`: Logical OR
- `and`: Logical AND
- `<`, `>`, `<=`, `>=`: Comparison operators
- `==`, `!=`: Equality operators
- `concat`: String concatenation

## Complete Examples

### Example 1: Simple Auto Insurance Model

**Model Configuration** (`auto_insurance_model.json`):
```json
{
  "liability": {
    "base": {
      "type": "fixed",
      "value": 77.02
    },
    "driver_age": {
      "type": "numerical",
      "value": "driver_age",
      "intervals": [null, "!default!", "[18, 25)", "[25, 35)", "[35, 50)", "[50, 65)", "[65, 100]"],
      "beta": [1.81, 1.81, 1.0, 1.8, 1.2, 1.0, 1.1, 1.3]
    },
    "vehicle_fuel_type": {
      "type": "categorical",
      "value": "vehicle_fuel_type",
      "categories": [null, "!default!", "diesel", "gasoline", "hybrid", "electric"],
      "beta": [1.0, 1.0, 1.0, 1.2, 1.0, 1.2, 1.3]
    },
    "min": {
      "type": "fixed",
      "value": 50.0
    },
    "max": {
      "type": "fixed",
      "value": 2500.0
    }
  }
}
```

**Usage:**
```python
from acturate.rating_engine.model import Model

# Create and load the model
pricing = Model()
pricing.load_model("model.json")

# Example quotes
quotes = [
    {
        "driver_age": 27,
        "vehicle_age": 10.09,
        "vehicle_fuel_type": "diesel"
    },
    {
        "driver_age": 50,
        "vehicle_age": 16.09,
        "vehicle_fuel_type": "gasoline"
    }
]

# Price each quote
for i, quote in enumerate(quotes):
    result = pricing.price(quote)
    print(f"Quote {i+1}: {result}")
```

### Example 2: Complex Model with Operations

**Model Configuration** (`complex_model.json`):
```json
{
  "comprehensive": {
    "base": {
      "type": "fixed",
      "value": 150.0
    },
    "age_factor": {
      "type": "operation",
      "operator": "*",
      "first_value": {
        "type": "numerical",
        "value": "driver_age",
        "intervals": [null, "!default!", "[18, 25)", "[25, 35)", "[35, 50)", "[50, 65)", "[65, 100]"],
        "beta": [1.5, 1.5, 1.0, 1.8, 1.2, 1.0, 1.1, 1.3]
      },
      "second_value": {
        "type": "fixed",
        "value": 1.05
      }
    },
    "vehicle_factor": {
      "type": "operation",
      "operator": "*",
      "first_value": {
        "type": "categorical",
        "value": "vehicle_fuel_type",
        "categories": [null, "!default!", "diesel", "gasoline", "hybrid", "electric"],
        "beta": [1.0, 1.0, 1.0, 1.2, 1.0, 1.2, 1.3]
      },
      "second_value": {
        "type": "numerical",
        "value": "vehicle_age",
        "intervals": [null, "!default!", "[0, 5)", "[5, 10)", "[10, 15)", "[15, 20)", "[20, 100]"],
        "beta": [1.0, 1.0, 1.0, 0.8, 1.0, 1.2, 1.5, 2.0]
      }
    },
    "min": {
      "type": "fixed",
      "value": 75.0
    },
    "base": {
      "type": "fixed",
      "value": 3000.0
    }
  }
}
```

**Usage:**
```python
from acturate.rating_engine.model import Model

# Create and load the model
pricing = Model()
pricing.load_model("complex_model.json")

# Complex quote with multiple factors
quote = {
    "driver_age": 35,
    "vehicle_age": 8.5,
    "vehicle_fuel_type": "hybrid"
}

result = pricing.price(quote)
print(f"Comprehensive premium: {result['comprehensive']}")
```

### Example 3: Multiple Coverages

**Model Configuration** (`multi_coverage_model.json`):
```json
{
  "liability": {
    "base": {
      "type": "fixed",
      "value": 100.0
    },
    "driver_age": {
      "type": "numerical",
      "value": "driver_age",
      "intervals": [null, "!default!", "[18, 25)", "[25, 35)", "[35, 50)", "[50, 65)", "[65, 100]"],
      "beta": [1.5, 1.5, 1.0, 1.8, 1.2, 1.0, 1.1, 1.3]
    }
  },
  "collision": {
    "base": {
      "type": "fixed",
      "value": 200.0
    },
    "vehicle_age": {
      "type": "numerical",
      "value": "vehicle_age",
      "intervals": [null, "!default!", "[0, 5)", "[5, 10)", "[10, 15)", "[15, 20)", "[20, 100]"],
      "beta": [1.0, 1.0, 1.0, 0.8, 1.0, 1.2, 1.5, 2.0]
    }
  },
  "comprehensive": {
    "base": {
      "type": "fixed",
      "value": 150.0
    },
    "vehicle_fuel_type": {
      "type": "categorical",
      "value": "vehicle_fuel_type",
      "categories": [null, "!default!", "diesel", "gasoline", "hybrid", "electric"],
      "beta": [1.0, 1.0, 1.0, 1.2, 1.0, 1.2, 1.3]
    }
  }
}
```

**Usage:**
```python
from acturate.rating_engine.model import Model

# Create and load the model
pricing = Model()
pricing.load_model("multi_coverage_model.json")

# Quote with all required data
quote = {
    "driver_age": 45,
    "vehicle_age": 12.5,
    "vehicle_fuel_type": "electric"
}

# Get pricing for all coverages
result = pricing.price(quote)
print("Premium breakdown:")
for coverage, premium in result.items():
    print(f"  {coverage}: ${premium:.2f}")
```
