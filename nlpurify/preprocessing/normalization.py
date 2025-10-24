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

from nlpurify.preprocessing.normalization_model import (
    WhiteSpace,
    CaseFolding,
    StopWords
)

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
