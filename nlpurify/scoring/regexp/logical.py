# -*- encoding: utf-8 -*-

"""
Creates an Extension to Perform Logical Operations

Logical operations like ``and`` or ``or`` can be implemented with the
module. This reduces manual intervention like using repeated for-loop
and/or conditional statements for the end user.
"""

from typing import List, Iterable

from nlpurify.scoring.baseclass import BaseLogicalOperator

class LogicalRegexp(BaseLogicalOperator):
    def __init__(self, string : str, *references : List[str]) -> None:
        super().__init__(string, *references)
