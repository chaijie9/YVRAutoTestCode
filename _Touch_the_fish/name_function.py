def get_formatted(first, last, middle=''):
    """
    Generate a neatly formatted full name.
    """
    if middle:
        full_name = first + " " + middle + " " + last
    else:
        full_name = first + " " + last
    return full_name.title()
