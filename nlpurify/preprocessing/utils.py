# -*- encoding: utf-8 -*-

"""
Utility Functions for Text Preprocessings
"""

import re

from pydantic import BaseModel
from nltk.tokenize import word_tokenize

class WordTokenize(BaseModel):
    """
    Tokenize text into word vectors using different types of methods
    to achieve cleaner text in desired formats.

    :param regexp, vanilla, tokenizer: Selection methods for different
        tokenization techniques. Set the value to ``regexp = True`` to
        tokenize text using regular expressions, for using pure Python
        based text tokenization use the ``vanilla = True`` method, and
        ``tokenizer = True`` (default) is for using external tokenizer
        functions like :func:`nltk.tokenize.word_tokenize` methods.
        The function will throw error if all of the values are set to
        true, and only one can be true at a time.
    """

    regexp    : bool = False
    vanilla   : bool = False
    tokenizer : bool = True

    # ? additional settings for regular expressions
    regexp_pattern : str = r"\w+"

    # ? additional settings for vanilla based methods
    vanilla_split_by : str = " "
    vanilla_getalpha : bool = False
    vanilla_getalnum : bool = False

    # ? additional settings for tokenizer based method
    tokenizer_language : str = "english"
    tokenizer_preserve_line : bool = False


    def apply(self, text : str) -> str:
        method = "regexp" if self.regexp else "vanilla" \
            if self.vanilla else "tokenizer" if self.tokenizer \
            else None # none should not be generated, validated values

        if method == "regexp":
            expression = re.compile(self.regexp_pattern)
            text = expression.findall(text)
        elif method == "vanilla":
            submethod = "retalpha" if self.vanilla_getalpha \
                else "retalnum" if self.vanilla_getalnum else None

            _functions = {
                "retalpha" : [
                    token for token in text.split(self.vanilla_split_by)
                    if token.isalpha()
                ],

                "retalnum" : [
                    token for token in text.split(self.vanilla_split_by)
                    if token.isalnum()
                ]
            }

            text = _functions.get(submethod, text)
        elif method == "tokenizer":
            text = word_tokenize(
                text,
                language = self.tokenizer_language,
                preserve_line = self.tokenizer_preserve_line
            )
        else:
            pass

        return text
