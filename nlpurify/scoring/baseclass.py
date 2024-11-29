# -*- encoding: utf-8 -*-

from typing import Iterable
from abc import ABC, abstractmethod

class BaseLogicalOperator(ABC):
    def __init__(self):
        pass


    @abstractmethod
    def scores(self, *args, **kwargs) -> Iterable[float]:
        """
        The Abstract Class Defination for Calculation of Individual Scores

        The individual scores are calculated in this function in the
        child methods and the abstract method is used as a placeholder.
        The abstract method ensures that all the child class use the
        same naming convention and thus can now safely invoke the
        ``evaluate`` method from the child class.
        """

        pass


    def evaluate(self, thresh : int, logic : str, operator : str = ">="):
        """
        Evaluate the Final Score using Logical Operators

        The operator like :attr:`>=`, :attr:`<=` is dynamic and thus
        provides additional controls to the logical operations as it
        can now be used to efficiently negate both the side of the
        curve for sequence matching. The operator is used internally
        and is evaluated using the :func:`eval()` to determine the
        final result and provide the score.

        ..versionchanged:: v2.0.0 gh#19 gh#18 gh#20
        The function ``scores()`` is now used to calculate the
        individual scores and the function ``evaluate()`` is now used
        to evaluate the final score using logical operators. The
        method is now available as a abstract method in the baseclass
        and returns an iterable values.

        :type  logic: str
        :param logic: The logical operator which is either :attr:`all`
            i.e., and condition and :attr:`any` which is or condition.

        :type  operator: str
        :param operator: The deterministic operator which can be used
            to efficiently control both the side of the curve for
            fuzzy scoring.
        """

        scores = self.scores()
        return eval(f"{logic}([score {operator} {thresh} for score in {scores}])")
