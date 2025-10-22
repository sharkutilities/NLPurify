# -*- encoding: utf-8 -*-

"""
Creates an Extension to Perform Logical Operations

Logical operations like ``and`` or ``or`` can be implemented with the
module. This reduces manual intervention like using repeated for-loop
and/or conditional statements for the end user.
"""

import re

from typing import List, Iterable

from nlpurify.scoring.baseclass import BaseLogicalOperator

class LogicalRegexp(BaseLogicalOperator):
    """
    An Extension to Perform Logical Operations for Regular Expression

    Regular expression are handy when searching for keywords in a
    sequence of text. This object combines multiple regular expressions
    and bound them under a logical operator to find sequence and score
    the same.

    :type  string: str
    :param string: The original string against which the reference
        values are to be checked and validated.

    :type  references: list
    :param references: A list of n-references against which fuzzy
        score is determined. The score is also a n-length array.
    """

    def __init__(self, string : str, *references : List[str]) -> None:
        super().__init__(string, *references)


    def scores(self) -> Iterable[float]:
        """
        Finds if the Expression is Found in the Statement

        Given n-references to search in the statement, the function,
        and returns ``100`` or ``0`` for each reference, for boolean
        values as scores.

        Caveat:: the score is either ``100`` if ``True`` else ``0``
        based on the regexp pattern matching.
        """

        found = [
            re.findall(pattern, self.string) for pattern in self.references
        ]

        return [ 100 if li else 0 for li in found ]
