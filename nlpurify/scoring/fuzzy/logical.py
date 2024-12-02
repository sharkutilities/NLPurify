# -*- encoding: utf-8 -*-

"""
Creates an Extension to Perform Logical Operations

Logical operations like ``and`` or ``or`` can be implemented with the
module. This reduces manual intervention like using repeated for-loop
and/or conditional statements for the end user.
"""

from typing import Iterable, List

from nlpurify.scoring.fuzzy.wrapper import fuzzy_score
from nlpurify.scoring.baseclass import BaseLogicalOperator

class LogicalFuzzy(BaseLogicalOperator):
    """
    The Logical Fuzzy is an Extension of Scoring for Logical Operation

    The logical operations can be integrated to search more than one
    reference string from a statement. This allows more control and
    also reduces repeated function call involving loops and other
    conditional statements.

    :type  string: str
    :param string: The original string against which the reference
        values are to be checked and validated.

    :type  references: list
    :param references: A list of n-references against which fuzzy
        score is determined. The score is also a n-length array.

    :type  method: str
    :param method: Amy of the supported method :func:`fuzzywuzzy.fuzz`
        module, defaults to "partial_ratio" method.

    .. code-block:: python

        statement = "a quick brown fox jumps over a lazy dog"

        # let's create an object to calculate and score the statement
        logical_fuzzy = nlpurify.fuzzy.LogicalFuzzy(statement, "quick", "foxy")

        # let's check the individual score of `quick` and `foxy` against statement
        print(logical_fuzzy.scores())
        >> [100, 75]

        # code to check if any of the value is <= 80
        print(logical_fuzzy.evaluate(80, logic = "any", operator = "<="))
        >> True # 100 <= 80 and 75 <= 80

        # code to check that all the values are >= 80 (default operator)
        print(logical_fuzzy.evaluate(80, logic = "all"))
        >> False # 100 >= 80 and 75 >= 80
    """

    def __init__(
        self,
        string : str,
        *references : List[str],
        method : str = "partial_ratio"
    ) -> None:
        super().__init__(string, *references)

        # mandatory keyword arguments which determines the fuzzy
        # the method is any of the supported argument of the fuzzy
        self.method = method


    def scores(self) -> Iterable[float]:
        """
        Calculate Fuzzy Score of Each Reference to Statement

        The internal function iterates for each reference string to
        score the similarity against the statement using the internal
        :func:`nlpurify.fuzzy.wrapper.fuzzy_score()` method.
        """

        return [
            fuzzy_score(self.string, reference, self.method)
            for reference in self.references
        ]
