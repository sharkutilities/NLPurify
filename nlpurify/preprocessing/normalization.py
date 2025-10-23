# -*- encoding: utf-8 -*-

"""
Text normalization is the process of converting text into a
consistent, standard, or "canonical" form. The goal is to reduce
randomness and variations in the text data, which helps in reducing
the overall number of unique words (the vocabulary size) and ensures
that different forms of the same word are treated as one.

The main goal is to provide a single function that can be used to
achieve normalization goals - popular methods are text cases (setting
lower or upper case to all the words), stopwords removal etc.

.. code-block:: python

    import NLPurify as nlpu

    ...
    text = " My   unCleaned text!!    "
    print(nlpu.preprocessing.normalize(text, ...))
    >> "my uncleaned text" # example of a cleaned text

The core methods is kept simple, and generic arguments are used which
are widely recognized/used by popular libraries.
"""

import os
import re

from pydantic import BaseModel
from abc import ABC, abstractmethod

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class _base_normalize(BaseModel, ABC):
    """
    Base Settings for Text Normalization with Field Validation
    """

    @abstractmethod
    def apply(self, text : str) -> str:
        pass


class WhiteSpace(_base_normalize):
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
        >> This is a uncleaned text with lots of extra white space.

    The model does not accept additional arguments and the function
    ``.apply()`` is used to clean and normalize white space from text.
    """

    strip   : bool = True
    lstrip  : bool = True
    rstrip  : bool = True
    newline : bool = True

    # ? if new line is true, then also allow to provide new line
    # which defaults to the operating system default
    newlinesep : str = os.linesep

    # ? remove multiple whitespace - uses regual expressions
    multispace : bool = True


    def apply(self, text : str) -> str:
        pattern = re.compile(r"\s+") # one/more white spaces

        # first - strip the white space from beginning and end of text
        if self.strip:
            text = text.strip()
        elif self.lstrip:
            text = text.lstrip()
        elif self.rstrip:
            text = text.rstrip()
        else:
            pass # no strip processing

        # second, remove new line characters from the text
        text = text.replace(self.newlinesep, " ") if self.newline \
            else text

        # third remove multiple white spaces from the string
        text = pattern.sub(" ", text) if self.multispace else text

        return text


class CaseFolding(_base_normalize):
    upper : bool = False
    lower : bool = True

    def apply(self, text : str) -> str:
        return text.upper() if self.upper else text.lower() if \
            text.lower() else text


class StopWords(_base_normalize):
    language   : str = "english"
    extrawords : list = []

    # ! by default, nltk library provides stopwords in lower case
    # however, we can override and set the value as per our case needs
    stopwords_in_uppercase : bool = False

    # ! removal of stop words is associated with word tokenization
    tokenize : bool = True


    def apply(self, text : str) -> str:
        stopwords_ = stopwords.words(self.language) + self.extrawords
        tokenized_ = word_tokenize(
            text, language = self.language, preserve_line = False
        ) if self.tokenize else text.split()

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
    The normalization function uses the in-built string function like
    :attr:`.strip()`, :attr:`.replace()` etc. to return a cleaner
    version. The following arguments are available for more control.
    A normalized texts may have the following properties:

        * It may not start or end with a white space character,
        * It may not have multiple spaces or spaces in the beginning
          or end of the scentence, and
        * It may not be spread in multiple lines (i.e., paragraph).

    All the above properties are desired, and can improve performance
    when used to train a large language model. Normalizaton of texts
    may also involve uniform case, typically :attr:`.lower()` that
    can be used to create a word vector.

    :type  text: str
    :param text: The base uncleaned text, all the operations are
        done on this text to return a cleaner version. The string can
        be single line, multi-line (example from "text area") and can
        have any type of escape characters.

    All the normalization techniques are put into one callable method
    which in turn uses ``pydantic`` models for data validation and
    settings management of each technique.

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

    Keyword Arguments
    -----------------

    The keyword arguments are used to toggle on/off each of the
    normalization techniques. Each technique is associated with an
    underlying dictionary which is defined under respective models.

    :rtype:  str
    :return: Return a cleaner version of string free of white
        characters as per user requirement.
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
