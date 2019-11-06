"""
Module with a function.
"""


def function(name="Gauss"):
    """
    Example function that prints a welcome message.

    Second paragraph should explain the function in more detail. Include
    citations to relevant literature and equations whenever possible. WRITE THE
    DOCSTRING FIRST since it helps reason about the design of your function and
    how you'll explain it.

    Parameters
    ----------
    name : str
        Name of the person to be greeted. Describe all parameters this way.

    Returns
    -------
    message : str
        The welcome message. Describe all return values this way.

    Examples
    --------

    >>> print(function())
    Welcome to the project, Gauss!

    """
    return f"Welcome to the project, {name}!"
