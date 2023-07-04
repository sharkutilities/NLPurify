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

from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


def processor(string : str) -> str:
    """
    A Simple Utility Function to Pre-Process a String

    The function inputs a string, and exports clean formatted string
    which is free of stop words (english) and the words are
    lemmatized, i.e. transformed to their base form.
    """

    tokens = word_tokenize(string.lower())
    filterted = [word for word in tokens if word not in stopwords.words("english")]
    lemmatized = [WordNetLemmatizer().lemmatize(word, "v") for word in filterted]
    
    return " ".join(lemmatized)


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
