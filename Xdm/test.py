from jinja2 import Template, UndefinedError, StrictUndefined

# 1. Using try-except to handle missing variables
template1 = Template("Hello {{ name }}! {{ greeting }}")
try:
    print("1. Try-except approach:")
    result = template1.render(name="John Doe")  # greeting is missing
    print(result)
except UndefinedError as e:
    print(f"Error: Missing variable - {e}")

print("\n" + "="*50 + "\n")

# 2. Using StrictUndefined to force error checking
template2 = Template("Hello {{ name }}! {{ greeting }}", undefined=StrictUndefined)
try:
    print("2. StrictUndefined approach:")
    result = template2.render(name="John Doe")  # greeting is missing
    print(result)
except UndefinedError as e:
    print(f"Error: Missing variable - {e}")

print("\n" + "="*50 + "\n")

# 3. Using default values
template3 = Template("Hello {{ name }}! {{ greeting | default('Good day') }}")
print("3. Default value approach:")
result = template3.render(name="John Doe")  # greeting will use default value
print(result)
