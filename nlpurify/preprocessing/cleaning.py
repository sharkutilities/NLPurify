# -*- encoding: utf-8 -*-

"""
A Set of Text Cleaning Methods
"""

import re

from functools import reduce

def multireplace(text : str, replacements : dict) -> str:
    """
    Replace Multiple Strings with Desired Text

    The function mimcs the methods of in-built ``.replace()`` method
    and extend functionality to either use raw text replacement or by
    using regular expressions to replace any types of strings.

    :type  text: str
    :param text: Raw text which requires to be cleaned, the return
        is a substring of the raw text with cleaned data.

    :type  replacements: dict
    :param replacements: An iterable dictionary of values to replace
        as key and replace with as values.

    Example Usage(s)
    ----------------

    Pass the raw text and desired replacements to perform a sub-string
    cleaning using the reduce operation like below.

    .. code-block:: python

        replacements = {"foo" : "bar", "baz" : "bar"}
        print(multireplace(
            "foo bar bar baz", replacements = replacements
        ))
        >> bar bar bar bar

    Note the order of the replacement is same as that of the given
    dictionary, consider the below example.

    .. code-block:: python

        replacements = {"foo" : "bar", "bar" : "baz"}
        print(multireplace(
            "foo bar bar baz", replacements = replacements
        ))
        >> baz baz baz baz

    :rtype:  str
    :return: A cleaned text replaced with the substrings as defined
        under the replacements dictionary.
    """

    return reduce(
        lambda s, p : re.sub(p[0], p[1], s),
        replacements.items(), text
    )
