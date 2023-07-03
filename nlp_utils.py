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

# from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

def processor(string : str) -> str:
    tokens = word_tokenize(string.lower())
    filterted = [word for word in tokens if word not in stopwords.words("english")]
    lemmatized = [WordNetLemmatizer().lemmatize(word, "v") for word in filterted]
    
    return " ".join(lemmatized)


def fuzzy_match(string : str, actual : str) -> int:
    pass
