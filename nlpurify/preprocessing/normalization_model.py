# -*- encoding: utf-8 -*-

"""
The Pydantic abstract base model is defined here which is extended
dynamically by the normalization function. The model can be used alone
or maybe used by the wrapper function.
"""

import os
import re

from pydantic import Field
from nltk.corpus import stopwords

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

    .. rubric:: Additional Note(s)

    The new line seperator is default to system, for windows based
    system the seperator is "\r\n" (i.e., ``CR LF`` notation), while
    for *nix based system it is "\n" (i.e., ``LF`` notation) default.
    """

    strip : bool = Field(
        default = True,
        description = "Strip of trailing white spaces from text."

    )
    lstrip : bool = Field(
        default = True,
        description = "Strip white spaces from beginning of text."

    )
    rstrip : bool = Field(
        default = True,
        description = "Strip white spaces from end of text."

    )
    newline : bool = Field(
        default = True,
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


class CaseFolding(NormalizerBaseModel):
    upper : bool = False
    lower : bool = True

    def apply(self, text : str) -> str:
        return text.upper() if self.upper else text.lower() if \
            text.lower() else text


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
