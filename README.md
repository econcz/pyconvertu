# CONVERTU - From/to Classification Converter

Tools for creating and converting between classification systems.

## Installation

```bash
pip install pyconvertu
```

## Quick example
python:  
```python
from convertu import cconv

print(cconv(to="iso3", text=["Czech Republic", "Slovakia"]))
```
bash:  
```bash
cconv -t iso3 'Czech Republic' 'Slovakia'
echo -e "Czech Republic\nSlovakia" | cconv -t iso3
```

## User Reference

```python
cconv(
    data=[...], json_file='...', info=False, dump=False,
    to="...", text="..." | ["...", "..."], *args, **kwargs
)
```

Convert text into a target classification using a JSON mapping, or return mapping/metadata (info/dump modes).

**Parameters:**  

`data` : *list[dict]*, optional  
A complete classification mapping provided directly as a list of dictionaries. If supplied without `json_file`, this data will be used in-memory for conversions without reading from disk.

`json_file` : *str*, optional  
Path to the classification JSON file. If not provided, the default bundled `classification.json` is used. When `data` is not supplied, this file is loaded and used as the source mapping. When `data` is supplied along with `json_file`, the data is written to `json_file`.

`info` : *bool*, default = *False*  
If *True*, return only metadata/sources entries. No conversion.

`dump` : *bool*, default = *False*  
If *True*, return the full mapping (filtered of metadata/sources). No conversion.

`to` : *str*  
Target field name to return from matched records (e.g., "iso3").

`text` : *str* | *list[str]*  
One string or a list of strings to convert. A single string input yields a single string output; a list yields a list.

**Classification passed via `data`**

The JSON must follow the same structure as the bundled classification.json.

```
[
    {
        "regex":    "^(.*afgh.*|\\s*AFG\\s*|\\s*AF\\s*|\\s*4\\s*)$",
        "name_en":  "Afghanistan",
        "name_fr":  "Afghanistan (l')",
        "iso3":     "AFG",
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

## License

MIT License — see the [LICENSE](LICENSE) file.
