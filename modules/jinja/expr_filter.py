def reverse_string(value) -> str:
    """Reverses the input string."""
    if not isinstance(value, str):
        raise TypeError("Input must be a string")
    return value[::-1]