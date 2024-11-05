<h1 align = "center">CHANGELOG</h1>

<div align = "justify">

All notable changes to this project will be documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [PEP0440](https://peps.python.org/pep-0440/)
styling guide. For full details, see the [commit logs](https://github.com/sharkutilities/pandas-wizard/commits).

## `PEP0440` Styling Guide

<details>
<summary>Click to open <code>PEP0440</code> Styilng Guide</summary>

Packaging for `PyPI` follows the standard PEP0440 styling guide and is implemented by the **`packaging.version.Version`** class. The other
popular versioning scheme is [`semver`](https://semver.org/), but each build has different parts/mapping.
The following table gives a mapping between these two versioning schemes:

<div align = "center">

| `PyPI` Version | `semver` Version |
| :---: | :---: |
| `epoch` | n/a |
| `major` | `major` |
| `minor` | `minor` |
| `micro` | `patch` |
| `pre` | `prerelease` |
| `dev` | `build` |
| `post` | n/a |

</div>

One can use the **`packaging`** version to convert between PyPI to semver and vice-versa. For more information, check
this [link](https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html).

</details>

## Release Note(s)

The release notes are documented, the list of changes to each different release are documented. The `major.minor` patch are indicated
under `h3` tags, while the `micro` and "version identifiers" are listed under `h4` and subsequent headlines. The legend for
changelogs are as follows:

  * 🎉 - **Major Feature** : something big that was not available before.
  * ✨ - **Feature Enhancement** : a miscellaneous minor improvement of an existing feature.
  * 🛠️ - **Patch/Fix** : something that previously didn’t work as documented – or according to reasonable expectations – should now work.
  * ⚙️ - **Code Efficiency** : an existing feature now may not require as much computation or memory.
  * 💣 - **Code Refactoring** : a breakable change often associated with `major` version bump.

### Version 2.0.0 | Advanced Functionalities - Fuzzy Scoring | WIP

The version is dedicated towards development and integration of `fuzzy` logic for sequence matching and scoring which
can be used for classification, scoring and identification.

  * **v0.0.3.dev3** - Developmental preview release that allows the developer/end user to use the fuzzy module. The version
    is tagged internally as development release.

### Version 1.0.0 | Conceptualization Phase | WIP

The conceptualization phase where the module objective, design patterns, and list of intended features for end-users are
listed. The below versions are minor/micro changes related to the stable release.

  * **v0.0.1.dev2** - Developmental Release, WIP
    * 🎉 Added more parametric control for text normalization like scentence case, strip line breaks.
    * 🛠️ Code compatibility with existing features to strip line breaks against strip characters commands.
    * ⚙️ All the different functionalities (like strip white space, etc.) are now moved under seperate private functions,
      this allows more control and easy management.
  * **v0.0.1.dev1** - Developmental Release, 18.08.2024
    * 🛠️ Legacy GitHub Gist code is added under submodule `nlpurify.legacy`. For more details and migration techniques,
      check [`#5`](https://github.com/sharkutilities/NLPurify/issues/5) for more informations.
    * 📝 Code documentation is hosted at [RTD/nlpurify](http://nlpurify.readthedocs.io/).
    * 🎉 Text normalization, i.e., cleaning of texts of unwanted characters like double space, multiple line breaks can
      now be cleaned by using function [normalizeText()](./nlpurify/normalize.py).
  * **v0.0.1.dev0** - Developmental Release, 17.08.2024
    * 🎉 Marks as the day when the ideation of the project started, and the name `NLPurify` is registered in PyPI.
    * ⚙️ This version is internal and have been deleted, this was released to block the package namespace.

</div>
