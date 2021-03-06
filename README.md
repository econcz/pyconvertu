# Tools for creation and conversion from/to desired classification (the default is ISO 3166-1)


This project was inspired by **[pycountry](https://pypi.org/project/pycountry/)** and  **[pycountry-convert](https://pypi.org/project/pycountry-convert/)** modules and is a port of the **Stata package** **[pyconvertu](https://ideas.repec.org/c/boc/bocode/s458892.html)** *(Stata module to convert a string variable into a classification from the default or user-provided JSON file with the help of Python 3)* written in Python 3 and ADO. The tools can, for example, be used together with **[pandas](https://pypi.org/project/pandas/)** to process **pandas.DataFrame()**, `data`, `index`, and / or `columns` (consult examples):

- ``convert(source_file=None, from_list=[], to_classification='')`` converts a **tuple** or a **list** into a classification from a built-in or user-defined JSON file using **regular expressions**.  
- ``classification(source_file=None, from_classification='')`` returns a **list** created from a classification.  
- ``info(source_file=None)`` prints metadata and sources from the built-in or user-defined JSON file.


## Parameters:
- `source_file` : *raw str* or *unicode*, optional.  
Relative or absolute path to the user-defined JSON file.
- `from_list` : *sequence* of *iterable*.  
Input data.
- `to_classification` : *str* or *unicode*.  
'name_en' (English name), 'name_fr' (French name), 'iso3' (ISO 3166-1 alpha-3), 'iso2' (ISO 3166-1 alpha-2), or 'isoN' (ISO 3166-1 numeric).
- `from_classification` : *str* or *unicode*.  
'name_en' (English name), 'name_fr' (French name), 'iso3' (ISO 3166-1 alpha-3), 'iso2' (ISO 3166-1 alpha-2), or 'isoN' (ISO 3166-1 numeric).


`source_file` (if defined) replaces the default classification (ISO 3166-1). The file must contain a list of dictionaries where `regex` is a compulsory key in each one. The default JSON file was prepared with the help of **[json](https://docs.python.org/3/library/json.html)** module:
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
            "[https://www.iso.org/iso-3166-country-codes.html](ISO 3166 COUNTRY CODES)",
            "[https://en.wikipedia.org/wiki/List_of_alternative_country_names](ALTERNATIVE NAMES)"
        ]
    }
]
```


## Returns:
- `l` : *list*.  
Processed data.


## Examples:
```
import pandas as pd
from pyconvertu import convert
from pyconvertu import classification
from pyconvertu import info

# Create a pandas dataframe with ISO 3166-1 alpha-3 as `index'
data = [1, 2, 3, 4, 5, 6, 7]
iso3 = convert(
    from_list=['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States'],
    to_classification='iso3'
)
pd.DataFrame(data, index=iso3)

# Create a pandas dataframe from available classifications
df = pd.DataFrame()
df['iso3'] = classification(from_classification='iso3')
for s in ['iso2', 'isoN', 'name_en', 'name_fr']:
    df[s] = convert(
        from_list=df['iso3'],
        to_classification=s
    )
print(df)

# Print information and metadata for the built-in JSON file and my_file.json
info()
info(source_file=r'my_file.json')
```