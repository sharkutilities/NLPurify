# -*- encoding: utf-8 -*-

"""
Creates an Extension to Perform Logical Operations

Logical operations like ``and`` or ``or`` can be implemented with the
module. This reduces manual intervention like using repeated for-loop
and/or conditional statements for the end user.
"""

from typing import List
from nlpurify.fuzzy.wrapper import fuzzy_score

class LogicalFuzzy:
    def __init__(
        self,
        string : str,
        *references : List[str],
        method : str = "partial_ratio"
    ) -> None:
        self.string = string

        # list of any n-reference strings for fuzzy scoring
        self.references = references

        # mandatory keyword arguments which determines the fuzzy
        # the method is any of the supported argument of the fuzzy
        self.method = method


    def _fuzzy_score_(self) -> list:
        return [
            fuzzy_score(self.string, reference, self.method)
            for reference in self.references
        ]
    

    def evaluate(self, thresh : int, logic : str, operator : str = ">="):
        """
        Evaluate the Final Score using Operators

        The operator like :attr:`>=`, :attr:`<=` is dynamic and thus
        provides additional controls to the logical operations as it
        can now be used to efficiently negate both the side of the
        curve for sequence matching. The operator is used internally
        and is evaluated using the :func:`eval()` to determine the
        final result and provide the score.

        :attr  logic: str
        :param logic: The logical operator which is either :attr:`all`
            i.e., and condition and :attr:`any` which is or condition.

        :attr  operator: str
        :param operator: The deterministic operator which can be used
            to efficiently control both the side of the curve for
            fuzzy scoring.
        """

        scores = self._fuzzy_score_()
        return eval(f"{logic}([score {operator} {thresh} for score in {scores}])")
