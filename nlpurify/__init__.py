# -*- encoding: utf-8 -*-

"""
Utility for Natural Language Processing (NLP) Techniques

Natural Language Processing (NLP) is the field of computer science to
process, understand and manipulate human language which are typically
well-defined and structured. The module is developed to provide a
one-stop solution for different types of processings like - feature
selection, feature extraction, pre-processing of texts (normalization,
cleaning, etc.) to provide a cleaner version of text that is easy for
computer to understand and integrate for further development.

The module uses various different external libraries to simplify the
tasks - check the module requirements for list of dependencies.
"""

# ? package follows https://peps.python.org/pep-0440/
# ? https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html
__version__ = "v2.1.0.dev0"

# init-time options registrations
from nlpurify.scoring import fuzzy
from nlpurify.scoring import regexp

from nlpurify.feature import (
    selection as feature_selection
)

from nlpurify.normalization import (
    normalize,
    strip_whitespace
)
