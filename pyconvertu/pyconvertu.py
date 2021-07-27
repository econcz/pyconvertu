"""
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Tools for creation or conversion of lists from/to desired classification
(the default is ISO 3166-1)
© econcz, 2021
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

This project was inspired
by **[pycountry](https://pypi.org/project/pycountry/)** and 
**[pycountry-convert](https://pypi.org/project/pycountry-convert/)**
modules and is a port of the **Stata package**
**[pyconvertu](https://ideas.repec.org/c/boc/bocode/s458892.html)**
*(Stata module to convert a string variable into a classification
from the default or user-provided JSON file with the help of Python 3)*
written in Python 3 and ADO. The tools can, for example,
be used together with **[pandas](https://pypi.org/project/pandas/)**
to process **pandas.DataFrame()**, `data`, `index`, and / or `columns`.

Parameters:
–––––––––––
    `source_file`         : *raw str* or *unicode*, optional
                            Relative or absolute path to the user-defined
                            JSON file.
    `from_list`           : *sequence* of *iterable*
                            Input data.
    `to_classification`   : *str* or *unicode*
                            'name_en' (English name), 'name_fr' (French name),
                            'iso3' (ISO 3166-1 alpha-3),
                            'iso2' (ISO 3166-1 alpha-2), or
                            'isoN' (ISO 3166-1 numeric).
    `from_classification` : *str* or *unicode*
                            'name_en' (English name), 'name_fr' (French name),
                            'iso3' (ISO 3166-1 alpha-3),
                            'iso2' (ISO 3166-1 alpha-2), or
                            'isoN' (ISO 3166-1 numeric).


`source_file` (if defined) replaces the default classification (ISO 3166-1).
The file must contain a list of dictionaries where `regex`
is a compulsory key in each one. The default JSON file was prepared
with the help of **[json](https://docs.python.org/3/library/json.html)**
module:
```
[
    {
        "regex":    "^(.*afgh.*|\\s*AFG\\s*|\\s*AF\\s*|\\s*4\\s*)$",
        "name_en":  "Afghanistan",                  # classification A
        "name_fr":  "Afghanistan (l')",             # classification B
        "iso3":     "AFG",                          # ...
        "iso2":     "AF",
        "isoN":     "4"
    },
    ...
    {
        "metadata": {
            "name_en": "English short name",
            "name_fr": "French short name",
            "iso3": "alpha-3 code",
            "iso2": "alpha-2 code",
            "isoN": "numeric"
        }
    },
    {
        "sources": [
            "[...](ISO 3166 COUNTRY CODES)",
            "[...](ALTERNATIVE NAMES)"
        ]
    }
]
```

Returns:
––––––––
    `l`  : *list*
           Processed data.
"""

import json
import os
import re
import sys

# User-defined Functions
def convert(
    source_file=r'' + sys.modules['pyconvertu'].__file__.replace(
        '__init__.py', 'classification.json'
    ),
    from_list=[], to_classification='',
    *args, **kwargs
):
    """
    Converts a list of strings (from_list) to classification
    (to_classification) based on a JSON file (source_file).
    """
    try:
        # load classification
        with open(os.path.expanduser(source_file)) as f:
            classification = list(filter(
                lambda d: not d.get('metadata') and not d.get('sources'),
                json.load(f)
            ))
        # convert list
        return list(map(
            lambda s:
                (lambda l, s: 
                    l[1].get(to_classification) if len(l) > 1 else l[0]
                )(
                    [s] + list(filter(
                        lambda d: re.search(
                            r'' + d.get('regex') + r'', s, flags=re.I|re.M
                        ),
                        classification
                    )),
                    str(s)
                ),
                from_list
            ))
    except:
        return {}

def classification(
    source_file=r'' + sys.modules['pyconvertu'].__file__.replace(
        '__init__.py', 'classification.json'
    ),
    from_classification='',
    *args, **kwargs
):
    """
    Creates a list of strings from classification
    (from_classification) based on a JSON file (source_file).
    """
    try:
        # load classification
        with open(os.path.expanduser(source_file)) as f:
            classification = list(filter(
                lambda d: not d.get('metadata') and not d.get('sources'),
                    json.load(f)
            ))
        # create list
        l = list(map(
            lambda d: d.get(from_classification),
                classification
            ))
        l.sort()
        return l
    except:
        return {}

def info(
    source_file=r'' + sys.modules['pyconvertu'].__file__.replace(
        '__init__.py', 'classification.json'
    ),
    *args, **kwargs
):
    """
    Returns a list based on a JSON file (source_file).
    """
    try:
        # load classification metadata
        with open(os.path.expanduser(source_file)) as f:
            metadata = list(filter(
                lambda d: d.get('metadata') or d.get('sources'),
                    json.load(f)
                ))
        # create list
        return list(map(
            lambda d: str(d),
                metadata
            ))
    except:
        return {}