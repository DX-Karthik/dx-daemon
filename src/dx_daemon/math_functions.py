import math

# 1. Basic Arithmetic Operators
print("--- Basic Arithmetic ---")
a = 15
b = 4

print(f"Addition (a + b): {a + b}")
print(f"Subtraction (a - b): {a - b}")
print(f"Multiplication (a * b): {a * b}")
print(f"Division (a / b): {a / b}")
print(f"Floor Division (a // b): {a // b}")  # Drops the decimal portion
print(f"Modulus/Remainder (a % b): {a % b}")  # Returns the remainder
print(f"Exponent/Power (b ** 2): {b ** 2}")  # 4 raised to power of 2


# 2. Built-in Math Module Functions
print("\n--- Math Module Functions ---")
number = 25.67

print(f"Square Root of 25: {math.sqrt(25)}")
print(f"Absolute Value of -10: {math.fabs(-10)}")
print(f"Floor (round down) of {number}: {math.floor(number)}")
print(f"Ceil (round up) of {number}: {math.ceil(number)}")
print(f"Factorial of 5: {math.factorial(5)}")


# 3. Geometric Formulas & Mathematical Constants
print("\n--- Geometry & Constants ---")
print(f"Value of Pi: {math.pi}")
print(f"Value of Euler's Number (e): {math.e}")

# Calculate Area of a Circle: area = pi * r^2
radius = 5
circle_area = math.pi * (radius ** 2)
print(f"Area of circle with radius {radius}: {circle_area:.2f}")

# Calculate Hypotenuse of a Right Triangle: c = sqrt(x^2 + y^2)
side_x = 3
side_y = 4
hypotenuse = math.hypot(side_x, side_y)
print(f"Hypotenuse of triangle (sides {side_x} and {side_y}): {hypotenuse}")


# 4. Trigonometry
print("\n--- Trigonometry ---")
# Trigonometric functions expect values in radians
angle_degrees = 45
angle_radians = math.radians(angle_degrees)

print(f"Sine of {angle_degrees}°: {math.sin(angle_radians):.4f}")
print(f"Cosine of {angle_degrees}°: {math.cos(angle_radians):.4f}")
