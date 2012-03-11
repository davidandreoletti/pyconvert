def enum(*sequential, **named):
    """
    Creates an "enum" type
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
