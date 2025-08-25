from   os        import path
from   re        import compile, Pattern, I, M, error as RegexError
from   typing    import Any
from   importlib import resources
from   json      import load, dump as save, JSONDecodeError

class ConvertUError(Exception):
    """
    Exception class for ConvertU-related errors.

    Raised when an error occurs during classification conversion,
    metadata retrieval, or parsing of external JSON files.
    Provides structured messaging and optional diagnostic tagging.

    Parameters
    ----------
    message : str, optional
        Human-readable description of the error. Defaults to a generic message.

    code : int or str, optional
        Optional error code or identifier for structured handling.

    Usage
    -----
    raise ConvertUError("Unsupported classification key", code=400)
    """
    def __init__(self, message: str       = "An error occurred in convertu",
                       code:    int | str | None = None):
        self.message = message
        self.code    = code
        full_message = f"{message} (Code: {code})" if code is not None         \
                                                   else message
        super().__init__(full_message)
        
    def __str__(self) -> str:
        return self.message if self.code is None                               \
                            else f"{self.message} [Code: {self.code}]"
    
    def as_dict(self) -> dict:
        return {"error": self.message, "code": self.code}

def _default_json_path() -> str:
    """
    Resolve the default path to the bundled `classification.json` file.
    """
    return str(resources.files("convertu").joinpath("classification.json"))

def _validate_data(obj: list[dict[str, Any]]) -> None:
    """
    Validate that `obj` conforms to the required structure:
    - at least one dict has key 'regex'    (value is a str );
    - exactly  one dict has key 'metadata' (value is a dict);
    - exactly  one dict has key 'sources'  (value is a list).
    """
    if not isinstance(obj, list) or not all(isinstance(d, dict) for d in obj):
        raise  ConvertUError("`data` must be a list[dict]")
    if not any(isinstance(d.get("regex"), str) and d.get("regex", "").strip()
             for d in obj):
        raise  ConvertUError("`data` must include at least one entry with "
                             "a non-empty 'regex' string")
    if sum(1 for d in obj if "metadata" in d                    and
                             isinstance(d["metadata"], dict)    and
                             d["metadata"])                     != 1:
        raise  ConvertUError("`data` must include exactly one non-empty "
                             "'metadata' dict")
    if sum(1 for d in obj if "sources"  in d                    and
                             isinstance(d["sources"], list)     and
                             d["sources"])                      != 1:
        raise  ConvertUError("`data` must include exactly one non-empty "
                             "'sources' list")

def cconv(
    data: list[dict] | None = None,  json_file: str             | None = None,
    info: bool              = False, dump:      bool                   = False,
    to:   str               = '',    text:      str | list[str] | None = None,
    *args, **kwargs
) -> str | list[str] | list[dict]:
    """
    Convert text into a target classification using a JSON mapping, or
    return mapping/metadata (info/dump modes).

    Parameters
    ----------
    data : list[dict], optional
        A complete classification mapping provided directly as a list of
        dictionaries. If supplied without `json_file`, this data will be
        used in-memory for conversions without reading from disk.

    json_file : str, optional
        Path to the classification JSON file. If not provided, the default
        bundled `classification.json` is used. When `data` is not supplied,
        this file is loaded and used as the source mapping. When `data` is
        supplied along with `json_file`, the data is written to `json_file`.

    info : bool, default = False
        If True, return only metadata/sources entries. No conversion.

    dump : bool, default = False
        If True, return the full mapping (filtered of metadata/sources).
        No conversion.

    to : str
        Target field name to return from matched records (e.g., "iso3").

    text : str | list[str]
        One string or a list of strings to convert. A single string input
        yields a single string output; a list yields a list.

    Returns
    -------
    str | list[str] | list[dict]
        - If `info=True`: list of metadata/sources dicts.
        - If `dump=True`: list of mapping dicts (no metadata/sources).
        - Otherwise: converted string(s). If no match is found, the original
          value is returned. If `text` is None, returns an empty list.
    """
    # retrieve the metadata/sources and classification
    if data is not None:                               # read from the argument
        _validate_data(data)
        if  json_file is not None:
            json_file = path.expanduser(json_file)
            try:
                with open(json_file, "w", encoding="utf-8") as f:
                    save(data, f, ensure_ascii=False, indent=2)
            except OSError as e:
                raise ConvertUError(f"Unable to write to {json_file}: {e}")
            return json_file
    else:                                              # read from the file
        if  json_file is None:
            json_file = _default_json_path()
        if  not path.isfile(json_file):
            raise ConvertUError(f"Classification file not found: {json_file}")
        try:
            with open(json_file, encoding="utf-8") as f:
                data = load(f)
        except JSONDecodeError as e:
            raise ConvertUError(f"Invalid JSON in {json_file}: {e}")
        except OSError as e:
            raise ConvertUError(f"Unable to read {json_file}: {e}")
        if  not isinstance(data, list):
            raise ConvertUError("Mapping JSON must be a list of objects")
    metadata                             = [
        d for d in data
        if isinstance(d, dict) and ('metadata'     in d or
                                    'sources'      in d)
    ]
    classification: list[dict[str, Any]] = [
        d for d in data
        if isinstance(d, dict) and ('metadata' not in d and
                                    'sources'  not in d)
    ]

    # return metadata/sources or classification
    if  info:
        return metadata                                # return metadata
    if  dump:
        return classification                          # return classification

    # process arguments
    if   text is None:
        items: list[str] = []
        single_input = False
    elif isinstance(text, str):
        items = [text]
        single_input = True
    elif isinstance(text, list) and all(isinstance(s, str) for s in text):
        items = text
        single_input = False
    else:
        raise ConvertUError("text must be str, list[str], or None")

    # precompile regex patterns once
    compiled: list[tuple[Pattern[str], dict[str, Any]]] = []
    for r in classification:
        p = r.get('regex')
        if  to in r and isinstance(p, str) and p:
            try:
                compiled.append((compile(p, I | M), r))
            except RegexError:
                continue
    if  items and not compiled:
        return text if single_input else items

    # convert compiled
    def convert_one(s: str) -> str:
        s = str(s)
        for p, r in compiled:
            if  p.search(s):
                val = r.get(to)
                return s if val is None else val       # return converted text
        return s                                       # return original  text

    result = [convert_one(s) for s in items]
    return result[0] if single_input else result
