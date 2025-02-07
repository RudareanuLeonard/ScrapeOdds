import re

def is_decimal_odd(text):
    decimal_pattern = r"^\d+\.\d{1,2}$"  # Matches decimal odds (e.g., 1.50, 2.00, 10.75)
    return bool(re.match(decimal_pattern, text))

# Test cases
test_cases = ["1.50", "2.00", "10.75", "3", "1.234", "abc", "2.5", "0.99", "100.0"]

for test in test_cases:
    print(f"{test}: {is_decimal_odd(test)}")
