# -*- encoding: utf-8 -*-

"""
Text normalization is the process of converting text into a
consistent, standard, or "canonical" form. The goal is to reduce
randomness and variations in the text data, which helps in reducing
the overall number of unique words (the vocabulary size) and ensures
that different forms of the same word are treated as one.

The main goal is to provide a single function that can be used to
achieve normalization goals - popular methods are text cases (setting
lower or upper case to all the words), stopwords removal etc. The
underlying function uses core Python string manipulation methods with
additional third party libraries (like :mod:`nltk`) to achieve text
normalization.

The core methods is kept simple, and generic arguments are used which
are widely recognized/used by popular libraries.
"""

import os
import re
import warnings

from nltk.corpus import stopwords
from pydantic import Field, model_validator

from nlpurify.preprocessing.utils import WordTokenize
from nlpurify.preprocessing._base import NormalizerBaseModel

class WhiteSpace(NormalizerBaseModel):
    """
    A Model to Normalize White Space (space, tabs, newlines) from Text

    Cleaning texts of white spaces like from beginning, end, and
    also multiple white spaces does not add any value to a text and
    should thus be removed to normalize the text.

    :param strip, lstrip, rstrip: Settings to strip white spaces from
        beginning or end of the string for normalization. By default,
        all the spaces are removed as they do not provide any
        additional information and is mostly an error in typing text.

    :param newline: Strip new line characters from a multiple line
        (i.e., a paragraph or text from "text area") to get one single
        text, defaults to True.

    :param newlinesep: A string value which defaults to the systems'
        default new line seperator ("\r\n" `CRLF` for windows, and
        "\n" `LF` for *nix based systems) to replace from string.

    :param multispace: Replace multiple spaces which often reduces the
        models' performance, defaults to True.

    A modular approach is now enabled which is derived from a base
    normalization class. The usage is as below:

    .. code-block:: python

        import nlpurify as nlpu
        model = nlpu.preprocessing.normalization.WhiteSpace()

        # let's define a multi-line uncleaned text
        text = '''
            This is a   uncleaned text    with lots of
           extra white
        space.
        '''

        print(model.apply(text)) # uses default settings
        >> "This is a uncleaned text with lots of extra white space."

    The model does not accept additional arguments and the function
    ``.apply()`` is used to clean and normalize white space from text.
    """

    strip : bool = Field(
        True,
        description = "Strip of trailing white spaces from text."
    )

    lstrip : bool = Field(
        True,
        description = "Strip white spaces from beginning of text."
    )

    rstrip : bool = Field(
        True,
        description = "Strip white spaces from end of text."
    )

    newline : bool = Field(
        True,
        description = "Strip any new line characters from text."

    )

    # ? if new line is true, then also allow to provide new line
    # which defaults to the operating system default
    newlinesep : str = Field(
        default = os.linesep,
        description = "Default line seperator based on system."
    )

    # ? remove multiple whitespace - uses regual expressions
    multispace : bool = Field(
        default = True,
        description = "Remove multiple spaces from text using regexp."
    )


    def apply(self, text : str) -> str:
        pattern = re.compile(r"[ \t]{2,}") # one/more white spaces/tab

        # first - strip the white space from beginning and end of text
        if self.strip:
            text = text.strip()
        else:
            if self.lstrip:
                text = text.lstrip()
            elif self.rstrip:
                text = text.strip()
            else:
                pass # todo raise invalid warning for combination

        # second, remove new line characters from the text
        if self.newline:
            text = text.replace(self.newlinesep, " ")

        # third remove multiple white spaces from the string
        if self.multispace:
            text = pattern.sub(" ", text)

        return text


    @model_validator(mode = "after")
    def model_validator(self) -> object:
        """
        Pydantic generic model validator which validates all the
        fields using the self.attribute parameter and is generic to
        the class.
        """

        s, ls, rs = self.strip, self.lstrip, self.rstrip

        if not s and all([ls, rs]):
            warnings.warn(
                "Both `lstrip`` and ``rstip`` is True. While "
                "the ``strip`` value is False, which results "
                "in same result when ``strip == True`` (default)."
            )

        if s and not all([ls, rs]):
            warnings.warn(
                "The ``strip`` is set to True, while one of "
                f"``lstrip == {ls}`` or ``rstrip == {rs}`` "
                "is set to False, which is ambiguous as "
                "attribute strip always has a precedence."
            )

        return self


class CaseFolding(NormalizerBaseModel):
    """
    A Model to Normalize Case Folding from Texts

    Case folding from raw data source is often in title case, or is in
    a mixed case which hinder the NLP/LLM model's performance. The
    general convention is to convert all to lower cases using native
    Python function :func:`lower()` which is available for strings.

    The class provides a pydantic model which does the same thing and
    when used in a pipeline provides robust and dynamic type checking
    and adheres to the normalization process.

    :param upper, lower: Either set the text to upper case, or to
        lower case as per user choice. Default configuration sets the
        value to lower case.
    """

    upper : bool = False
    lower : bool = True

    def apply(self, text : str) -> str:
        """
        Normalize the text into either all small case or upper case
        as per the forward models' need.
        """

        return text.upper() if self.upper else text.lower() if \
            text.lower() else text

    @model_validator(mode = "after")
    def model_validator(self) -> object:
        """
        Validate all the attributes of the class, and raise an error
        when the validation fails for any given combination below.

        :raises AssertionError: Error is raised when both the
            attribute ``upper`` and ``lower`` is set to True.
        """

        assert sum([self.upper, self.lower]) == 1, \
            "Both the value cannot be True."

        return self


class StopWords(NormalizerBaseModel):
    language   : str = "english"
    extrawords : list = []

    # ! by default, nltk library provides stopwords in lower case
    # however, we can override and set the value as per our case needs
    stopwords_in_uppercase : bool = False

    # ! removal of stop words is associated with word tokenization
    tokenize : bool = True
    tokenize_config : WordTokenize = WordTokenize()


    def apply(self, text : str) -> str:
        stopwords_ = stopwords.words(self.language) + self.extrawords
        tokenized_ = self.tokenize_config.apply(text) \
            if self.tokenize else text.split()

        # case folding of stopwords in upper/lower case as per need
        stopwords_ = list(map(
            lambda x : x.upper(), stopwords_
        )) if self.stopwords_in_uppercase else stopwords_

        return " ".join([
            word for word in tokenized_ if word not in stopwords_
        ])


def normalize(
        text : str,
        whitespace : bool = True,
        casefolding : bool = True,
        stopwords : bool = True,
        **kwargs
    ) -> str:
    """
    The normalization function provides an one-stop solution for all
    types of basic text normalization - white space, case folding and
    stop words removal each of which can be toggled on/off as per
    enduser's need. A normalized text may have the following
    properties:

        * It may not start or end with a white space character,
        * It may not have multiple spaces or spaces in the beginning
          or end of the scentence, and
        * It may not be spread in multiple lines (i.e., paragraph).

    All the above properties are desired, and can improve performance
    when used to train a large language model. Normalizaton of texts
    may also involve uniform case, typically :attr:`string.lower()`
    that can be used to create a word vector.

    :type  text: str
    :param text: The base uncleaned text, all the operations are
        done on this text to return a cleaner version. The string can
        be single line, multi-line (example from "text area") and can
        have any type of escape characters.

    All the normalization techniques are put into one callable method
    which in turn uses :mod:`pydantic` models for data validation and
    settings management of each technique. Below are the toggles:

    :type  whitespace: bool
    :param whitespace: A technique  that normalizes the white space
        from the underlying texts. A text with multiple white spaces
        increases the processing load of a NLP/LLM model that can hurt
        performance. White spaces in a text includes spaces, tabs and
        new lines which is the primary delimiter of a NLP/LLM model.

    :type  casefolding: bool
    :param casefolding: Technique to normalize cases from a string to
        a desired format, i.e., either all caps or all in small case.
        It is always a good practice to convert all the raw text into
        small case and then send for further modeling.

    :type  stopwords: bool
    :param stopwords: A stop word is a common high-frequency word like
        "the", "and", etc. that have no meaning of their own. Removing
        the stop words can often improve the model efficiency, default
        to True.

    .. rubric:: Keyword Arguments

    The keyword arguments are used to toggle on/off each of the
    normalization techniques. Each technique is associated with an
    underlying dictionary which is defined under respective models.

    Please refer to the underlying functions for detailed keyword
    arguments associated with each normalization techique(s) as below:

        *   **whitespace** : Associated with white space removal, the
            function takes in arguments associated with native string
            functions of Python, check :class:`WhiteSpace` for more
            informations.

        *   **casefolding** : Associated to set uniform text case, the
            model either converts all the string to upper case or in
            lower case using Python native string functions, for
            more details check signature of :class:`CaseFolding` class.

        *   **stopwords** : Associated with white stop words removal,
            check the underlying validation class is :class:`StopWords`
            for more details.

    .. rubric:: Code Example(s)

    The default configuration is (most of the time) the best normal
    form of the text, which is widely used. This can be achieved using
    the default setting like below.

    .. code-block:: python

        import nlpurify as nlpu

        ...
        text = " My   unCleaned text!!    "
        print(nlpu.preprocessing.normalize(text, ...))
        >> "my uncleaned text" # example of a cleaned text

    .. rubric:: Return Data

    :rtype:  str
    :return: Return a cleaner version of string which is normalized
        and treated thus providing a better performance for forward
        NLP/LLM based modelling.
    """

    whitespace_model = WhiteSpace(**{
        k : kwargs.get(k, WhiteSpace.model_fields[k].default)
        for k in list(WhiteSpace.model_fields.keys())
        if k in kwargs.keys()
    })

    casefolding_model = CaseFolding(**{
        k : kwargs.get(k, CaseFolding.model_fields[k].default)
        for k in list(CaseFolding.model_fields.keys())
        if k in kwargs.keys()
    })

    stopwords_model = StopWords(**{
        k : kwargs.get(k, StopWords.model_fields[k].default)
        for k in list(StopWords.model_fields.keys())
        if k in kwargs.keys()
    })

    text = whitespace_model.apply(text) if whitespace else text
    text = casefolding_model.apply(text) if casefolding else text
    text = stopwords_model.apply(text) if stopwords else text

    return text
