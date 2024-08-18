# -*- encoding: utf-8 -*-

"""
Module Involved to Normalization of Text

The normalization of text involves cleaning of text/strings from
unwanted characters like double spacing, double line breaks to single
line breaks, etc. A single functional approach is designed to handle
all such user's requests.
"""

import os

def _strip_whitespace(
        text : str,
        strip_whitespace : bool,
        strip_whitespace_start : bool,
        strip_whitespace_final : bool
    ) -> str:
    """
    Normalive Text of White Spaces from Beginning and End

    The normal text behavior is that they do not contain a white space
    characters at the beginning and end of the string.
    """

    _choice = {
        "strip_whitespace_start" : text.lstrip(),
        "strip_whitespace_final" : text.rstrip(),

        # ? setting default i.e., no strip when all false
        "default" : text
    }

    if strip_whitespace:
        # has priority over `strip_whitespace_*` atrributes
        text = text.strip()
    else:
        choice = "strip_whitespace_start" if strip_whitespace_start \
            else "strip_whitespace_final" if strip_whitespace_final \
            else "default"

        text = _choice[choice]

    return text


def normalizeText(
        text : str,
        replace_double_space : bool = True,
        replace_double_line_breaks : bool = True,
        **kwargs
    ) -> str:
    """
    Normalize a Given String with User-Defined Configurations

    The normalization function uses the in-built string function like
    :attr:`.strip()`, :attr:`.replace()` etc. to return a cleaner
    version. The following arguments are available for more control.

    :type  text: str
    :param text: The base uncleaned text, all the operations are
        done on this text to return a cleaner version. The string can
        be single line, multi-line (example from "text area") and can
        have any type of escape characters.

    :type  replace_double_space: bool
    :param replace_double_space: A common type of uncleaned text
        format includes double space (white characters), which can be
        directly cleaned without compromising informations. Defaults
        to True.

    :type  replace_double_line_breaks: bool
    :param replace_double_line_breaks: Double line breaks are common
        in texts containing paragraphs. This can be easily replaced
        with a single line break character set. Defaults to True.
        NOTE: The line break is dependent on the operating system:
        in windows it is "\\r\\n" or "CR LF" while in *nix system it
        is always "\\n" or "LF". To answer this, the program considers
        the default line break based on the operating system the code
        is running. To override this - use the keyword argument.

    **Keyword Arguments**
        * **strip_whitespace** (*bool*): Strip white space from the
          beginning or end of the text. Defaults to True. Alternate
          keyword terms are :attr:`strip_whitespace_start` and
          :attr:`strip_whitespace_final` which cleans white space from
          the beginning or end of string only respectively. The
          attribute :attr:`strip_whitespace` has priority over its
          alternates and ignores alternates if set to True.
        * **strip_whitespace_inline** (*bool*): This is an extension
          of the :attr:`strip_whitespace` that iterates for each line
          and strips the white spaces at the beginning and end of each
          line. This is useful when the text spans multiple lines.
          Defaults to True. Similar to :attr:`strip_whitespace` the
          alternate arguments are :attr:`strip_whitespace_inline_start`
          and :attr:`strip_whitespace_inline_start` which if True
          strips only the beginning or the ending white space from
          each line.
        * **line_break_seperator** (*str*): The end line character
            which is either "\\r\\n" for windows or "\\n" for *nix
            based systems. By default defaults to running operating
            systems default.
    """

    strip_whitespace = kwargs.get("strip_whitespace", True)
    strip_whitespace_inline = kwargs.get("strip_whitespace", True)

    if replace_double_space:
        # ? can compile with regex:: `re.compile(r"\s+"")`
        text = text.replace("  ", " ")

    if replace_double_line_breaks:
        # get the keyword argument for line break seperator,
        # or else get the os default, value is doubled internally
        line_break_seperator = kwargs.get("line_break_seperator", os.linesep)
        text = text.replace(line_break_seperator * 2, line_break_seperator)

    # ? related alternate terms to `strip_whitespace`
    strip_whitespace_start = kwargs.get("strip_whitespace_start", False)
    strip_whitespace_final = kwargs.get("strip_whitespace_final", False)

    # ? related alternate terms to `strip_whitespace_inline`
    strip_whitespace_inline_start = kwargs.get("strip_whitespace_inline_start", False)
    strip_whitespace_inline_final = kwargs.get("strip_whitespace_inline_final", False)

    if any([strip_whitespace, strip_whitespace_start, strip_whitespace_final]):
        # white space character from the string is to be removed
        text = _strip_whitespace(
            text,
            strip_whitespace = strip_whitespace,
            strip_whitespace_start = strip_whitespace_start,
            strip_whitespace_final = strip_whitespace_final
        )

    if any([strip_whitespace_inline, strip_whitespace_inline_start, strip_whitespace_inline_final]):
        # white space character from the string is to be removed
        text = "\n".join([
            _strip_whitespace(
                line,
                strip_whitespace = strip_whitespace_inline,
                strip_whitespace_start = strip_whitespace_inline_start,
                strip_whitespace_final = strip_whitespace_inline_final
            )
            for line in text.splitlines()
        ])

    return text
