# -*- encoding: utf-8 -*-

"""
Base Class and Field Validators for Preprocessing of Raw Texts
"""

from typing import Any
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, model_validator

class NormalizerBaseModel(BaseModel, ABC):
    """
    Abstract base model with field validations and methods for all
    types of data normalization. The abstract method is defined in a
    way that all the inherited objects follow the same signature, and
    maintain the same methods and attributes.

    :type  name: str
    :param name: A unique name for the model to be identified, which
        can be either user-defined or defaults to class name.

    .. rubric:: Class Signature

    The base class is defined with specific signature to mimic a model
    that has the method ``.apply()`` which is equivalent to fit and
    transform methods of a machine learning model.
    """

    name : str = Field(
        default = None,
        description = "Set the model name, or default to class name"
    )


    @abstractmethod
    def apply(self, text : str) -> str:
        """
        A abstract method ``.apply()`` that takes in any string value
        that needs to be converted. The apply function makes the same
        model to be used for n-elements using a processing engine.

        :type  text: str
        :param text: Any string value that needs to be normalized, the
            method may also extend unique properties of the child.

        .. rubric:: Return Value

        :rtype:  str
        :return: Returns a normalized text which is as per the child
            class properties and attributes.
        """

        pass


    @model_validator(mode = "before")
    @classmethod
    def __set_name__(cls, data : Any) -> Any:
        """
        A private method to define populate the name of the model
        which when not defined defaults to the class name.
        """

        name = cls.__name__

        if isinstance(data, dict) and data.get("name") is None:
            data["name"] = name

        return data


    class Config:
        """
        Pydantic configuration, which when used with an instance of an
        abstract class handles the potential validation errors with
        complex data types of fields.
        """

        arbitrary_types_allowed = True
