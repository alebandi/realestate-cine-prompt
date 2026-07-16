SEPARATOR_WIDTH = 60


def separator():
    return "=" * SEPARATOR_WIDTH


def prompt_fields(fields):
    """Collect user input for each field.

    ``fields`` is an iterable of ``(name, label)`` pairs. Returns a dict
    mapping each field name to the entered value.
    """
    return {name: input(f"{label}: ") for name, label in fields}


def print_boxed(title, body):
    line = separator()
    print("\n" + line)
    print(title)
    print(line)
    print(body)
    print(line)
