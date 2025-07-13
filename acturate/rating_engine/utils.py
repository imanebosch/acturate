import re


def is_in_interval(number: float, interval: str) -> bool:
    # Extract numbers from the interval string

    match = re.match(r"\[\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)", interval)
    if not match:
        raise ValueError(f"Invalid interval format: {interval}")

    num1, num2 = map(float, match.groups())

    # Check if the number is within the interval
    return num1 <= number < num2
