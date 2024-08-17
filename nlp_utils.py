# -*- encoding: utf-8 -*-

"""
A set of utility function related to natural language
processing. In addition to the basic libraries, the module
requires the following corpus from `nltk` library:
  * `stopwords` : used to remove stop words from a given
                  strings. Currently using the function for
                  pre-processing.
                  
In addition, need some additional libraries like `fuzzywuzzy`
and `python-Levenshtein` using the following:

```python
pip install fuzzywuzzy
pip install python-Levenshtein
```

@author: Debmalya Pramanik
"""

import re

from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


def processor(string : str, text_process : bool = False, **kwargs) -> str:
    """
    A Simple Utility Function to Pre-Process a String

    The function inputs a string, and exports clean formatted string
    which is free of stop words (english) and the words are
    lemmatized, i.e. transformed to their base form.

    :type  string: str
    :param string: Base string on which various `nltk` functions are
                   applied to clean unwanted informations.

    :type  text_process: bool
    :param text_process: Should the base string be  formatted using
                         `text_process()`. Defaults to False.
    """

    tokens = word_tokenize(string.lower())
    filterted = [word for word in tokens if word not in stopwords.words("english")]
    lemmatized = [WordNetLemmatizer().lemmatize(word, "v") for word in filterted]
    
    return text_processor(" ".join(lemmatized), **kwargs) if text_process else " ".join(lemmatized)


def fuzzyMatch(string : str, reference : str, method : str = "partial_ratio") -> int:
    """
    Calculate a Percentage Similarity between `string` and `reference` Text

    Using the `fuzzywuzzy.fuzz()` method, the function calculates the percentage of
    similarity between two text data. There are various methods available which can
    be declared via `method` parameter. However, `partial_ratio` is great when
    we want to match a text with partial data. For example, we want to find all the
    strings which have the word 'annonymous' but the spelling, position may be
    different in each case.
    """

    method = {
        "ratio" : fuzz.ratio,
        "partial_ratio" : fuzz.partial_ratio,
        "token_sort_ratio" : fuzz.token_sort_ratio
    }.get(method)

    return method(reference, string)


def text_processor(string : str, **kwargs) -> str:
    """
    Uses String Methods to Clean a String

    An extension of the `processor` function, which uses the in-built
    python string methods to clear string contents. The function can
    be called seperatly, or pass `text_process = True)` in `processor`.
    More information on in-built string methods is available here:
    https://www.programiz.com/python-programming/methods/string.

    # ! Function is not yet optimized when used in conjunction.

    :type  string: str
    :param string: Base string which needs formatting. The string
                   is converted into lower case. If passed from
                   ! `processor`this step is repeated.
                   TODO fix when passed through parent function.

    Keyword Arguments
    -----------------
        * *isalnum* (bool): Only keep `alpha-numeric` charecters in the
          string. Defaults to False.
        * *isalpha* (bool): Only keep `alphabets` charecters in the
          string. Defaults to False.
    """

    isalnum = kwargs.get("isalnum", False)
    isalpha = kwargs.get("isalpha", False)

    string = re.sub("[^a-zA-Z0-9 \n\.]", "", string)
    string = string.lower().split()

    if isalnum:
        string = [s for s in string if s.isalnum()]
    elif isalpha:
        string = [s for s in string if s.isalpha()]
    else:
        pass # no processing required

    string = " ".join(string)
    return string.replace("  ", " ").strip() # remove extra spaces
