# calculate_stats.py
"""
A script that calculates the basic statistical metrics of a list of numbers.
"""

def analyze_numbers(numbers):
    if not numbers:
        return None

    total_sum = sum(numbers)
    count = len(numbers)
    average = total_sum / count
    highest = max(numbers)
    lowest = min(numbers)
    median = sorted(numbers)[len(numbers) // 2]

    return {
        "sum": total_sum,
        "count": count,
        "average": average,
        "max": highest,
        "min": lowest,
        "median": median
    }

def main():
    sample_data = []
    print("Enter 5 numbers to analyze:")
    while len(sample_data) < 5:
        entry = input(f"Number {len(sample_data) + 1}: ")
        try:
            number = float(entry)
            if number < 0:
                print("Negative numbers are not allowed. Please enter 0 or greater.")
                continue
            sample_data.append(number)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    results = analyze_numbers(sample_data)

    print(f"\nAnalyzing data pool: {sample_data}\n")
    for key, value in results.items():
        print(f"{key.capitalize()}: {value}")

if __name__ == "__main__":
    main()
