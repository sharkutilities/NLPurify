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
        description = """
        Strip white spaces from both the beginning and the end of the
        string for normalization. By default, all the spaces are
        removed as they do not provide any additional information for
        a LLM/NLP based models and reduces token counts.

        When the attribute is set to ``True`` the alternate parameters
        :attr:`lstrip` and :attr:`rstrip` is ignored, check model
        validator for more information. This uses the Python in-built
        string function as in example below:

        .. code-block:: python

            text = " this is a long text   "
            print(text.strip())
            >> 'this is a long text'

        Further customization like specifying alternate set of
        characters to be removed from the string is also supported by
        using the :attr:`strip_chars` attribute, for more information
        check `docs <https://docs.python.org/3/library/stdtypes.html#str.strip>`_.
        """
    )

    lstrip : bool = Field(
        True,
        description = """
        When set to true (default) removes the leading white characters
        from the string, or specify alternate set using
        :attr:`strip_chars` attribute.
        """
    )

    rstrip : bool = Field(
        True,
        description = """
        When set to true (default) removes the trailing white
        characters from the string, or specify alternate set using
        :attr:`strip_chars` attribute.
        """
    )

    strip_chars : str = Field(
        None,
        description = """
        Custom set characters to be removed from the string. The
        argument is not a "prefix" or a "suffix" but a combination of
        all the values to be stripped. Check
        `docs <https://docs.python.org/3/library/stdtypes.html#str.strip>`_
        for more information.
        """
    )

    newline : bool = Field(
        True,
        description = """
        Strip new line characters from a multiple line (i.e., a
        paragraph or text from "text area") to get one single text,
        defaults to True. By default, :attr:`strip` removes new lines
        from the beginning and end, while this argument using string
        replace method to remove within lines - useful when the source
        text is paragraphed and needs to be cleaned.
        """

    )

    # ? if new line is true, then also allow to provide new line
    # which defaults to the operating system default
    newlinesep : str = Field(
        default = os.linesep,
        description = """
        A string value which defaults to the systems' default new line
        seperator ("\\r\\n" `CRLF` for windows, and "\\n" `LF` for
        *nix based systems) to replace from string.
        """
    )

    # ? remove multiple whitespace - uses regual expressions
    multispace : bool = Field(
        default = True,
        description = """
        Replace multiple spaces using regular expressions, which often
        reduces the models' performance, defaults to True.
        """
    )


    def apply(self, text : str) -> str:
        pattern = re.compile(r"[ \t]{2,}") # one/more white spaces/tab

        # first - strip the white space from beginning and end of text
        if self.strip:
            text = text.strip(chars = self.strip_chars)
        else:
            if self.lstrip:
                text = text.lstrip(chars = self.strip_chars)
            elif self.rstrip:
                text = text.strip(chars = self.strip_chars)
            else:
                pass # error is raised during model assertion

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

        :raises UserWarning: A warning is raised when the parameter
            does not follow specified directive. It is recommended to
            check the attribute settings before using :func:`.apply()`
            or it might generated unwanted output.
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
    a mixed case which may hinder the NLP/LLM model's performance. The
    general convention is to convert all to lower cases using native
    Python function :func:`lower()` which is available for strings.
    """

    upper : bool = Field(
        False,
        description = """
        Convert the text to upper case and return the text without
        altering other things. Defaults to False, the class converts
        the text to lower case which is recommended in LLM/NLP models.
        """
    )

    lower : bool = Field(
        True,
        description = """
        Convert the contents fof the text to lower case (default) for
        an easy forward integration with LLM/NLP based models.
        """
    )

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
    """
    Normalize Raw Texts from Stop Words using NLTK Corpus

    The model uses the :mod:`nltk.corpus` to check the valid stopwords
    that when removed from a text improves an NLP/LLM models'
    performance. By default, the model is set to use the stopwords in
    the English language.
    """

    language : str = Field(
        "english",
        description = """
        A valid language name which is available and defined under
        :func:`nltk.corpus.stopwords`, defaults to the English. To see
        a valid list of languages follow below.

        .. code-block:: python

            import nltk

            # download the corpus if not already available
            # nltk.download("stopwords")
            from nltk.corpus import stopwords

            # once downloaded and available, check available list:
            print(stopwords.fileids())

        The code block is dependent on :mod:`nltk` for more information
        check `docs <https://www.nltk.org/index.html>`_.
        """
    )

    extrawords : list = Field(
        [],
        description = """
        The model gives the flexibility to add extra words which will
        be treated as stopwords which are not already defined under
        the :func:`nltk.corpus.stopwords` function. This can be
        helpful in dynamic debuging and quick manipulation of text to
        check forward models performance.
        """
    )

    # ..versionadded:: 2025-10-24 - also allow words to be excluded
    excludewords : list = Field(
        [],
        description = """
        Opposite to ``extrawords`` this attribute helps in updating
        the stopwords by removing/excluding words from the already
        defined words in ``stopwords.words(self.language)`` list.
        """
    )

    # ! by default, nltk library provides stopwords in lower case
    # however, we can override and set the value as per our case needs
    stopwords_in_uppercase : bool = False

    # ! removal of stop words is associated with word tokenization
    tokenize : bool = True
    tokenize_config : WordTokenize = WordTokenize()


    def apply(self, text : str) -> str:
        tokenized_ = self.tokenize_config.apply(text) \
            if self.tokenize else text.split()

        return " ".join([
            word for word in tokenized_ if word not in self.stopwords_
        ])


    @property
    def stopwords_(self) -> list:
        return list(map(
            lambda x : x.upper() if self.stopwords_in_uppercase else x.lower(),
            (
                set(stopwords.words(self.language) + self.extrawords)
                - set(self.excludewords)
            )
        ))


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
