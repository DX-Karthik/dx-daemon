# number_crunch.py
"""
A script that prompts for three integers and reports number-theory metrics
(sum, product, GCD, LCM) plus a per-number prime check and factorization,
displaying the results in aligned tables.
"""

import math


def _is_prime(n):
    n = abs(n)
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def _prime_factors(n):
    n = abs(n)
    factors = []
    if n < 2:
        return factors
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def analyze_integers(numbers):
    if not numbers:
        return None

    per_number = []
    for value in numbers:
        per_number.append({
            "value": value,
            "is_prime": _is_prime(value),
            "factorization": _prime_factors(value),
        })

    return {
        "sum": sum(numbers),
        "product": math.prod(numbers),
        "gcd": math.gcd(*numbers),
        "lcm": math.lcm(*numbers),
        "per_number": per_number,
    }


def _format_table(headers, rows):
    columns = list(zip(headers, *rows)) if rows else [(h,) for h in headers]
    widths = [max(len(str(cell)) for cell in column) for column in columns]

    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def render(cells):
        padded = [" " + str(cell).ljust(w) + " " for cell, w in zip(cells, widths)]
        return "|" + "|".join(padded) + "|"

    lines = [border, render(headers), border]
    lines.extend(render(row) for row in rows)
    lines.append(border)
    return "\n".join(lines)


def _factorization_str(factors):
    if not factors:
        return "-"
    return " x ".join(str(f) for f in factors)


def display_results(numbers, results):
    print(f"\nResults for {numbers}\n")

    aggregate_rows = [
        ("Sum", results["sum"]),
        ("Product", results["product"]),
        ("GCD", results["gcd"]),
        ("LCM", results["lcm"]),
    ]
    print(_format_table(("Metric", "Value"), aggregate_rows))
    print()

    per_number_rows = [
        (
            entry["value"],
            "Yes" if entry["is_prime"] else "No",
            _factorization_str(entry["factorization"]),
        )
        for entry in results["per_number"]
    ]
    print(_format_table(("Number", "Prime?", "Factorization"), per_number_rows))


def main():
    numbers = []
    print("Enter 3 integers to crunch:")
    while len(numbers) < 3:
        entry = input(f"Number {len(numbers) + 1}: ")
        try:
            numbers.append(int(entry))
        except ValueError:
            print("Invalid input. Please enter a whole number (integer).")

    results = analyze_integers(numbers)
    display_results(numbers, results)


if __name__ == "__main__":
    main()
