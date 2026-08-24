class DCYNValidationError(ValueError):
    """Raised when a value is not a valid Yes/No response."""


def to_boolean(value):
    if value == "Yes":
        return True

    if value == "No":
        return False

    raise DCYNValidationError("Value must be exactly 'Yes' or 'No'.")