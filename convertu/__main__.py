from   __future__ import annotations
import signal
import sys
import argparse
from   convertu   import cconv, __version__
from   typing     import Any
from   json       import dumps

def _print_human_readable(obj: Any) -> None:
    """
    Pretty-print JSON-like Python objects with UTF-8 characters preserved.
    """
    print(dumps(obj, ensure_ascii=False, indent=2))

def main() -> int:
    # make SIGPIPE behave like a normal EOF on Unix
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
      
    # prefer UTF-8 on stdout for consistent output
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(
        description="Convert from/to the desired classification."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"%(prog)s {__version__}",
        help="Show version and exit."
    )
    parser.add_argument(
        "-s", "--source", dest="source", default=None, metavar="PATH",
        help="Path to the classification JSON file (default: bundled file)."
    )
    parser.add_argument(
        "-t", "--to", dest="to", default=None, metavar="FIELD",
        help="E.g., iso3, iso2, name_en (Required unless --info/--dump)."
    )
    parser.add_argument(
        "--info", action="store_true",
        help="Show metadata and sources in human-readable form."
    )
    parser.add_argument(
        "--dump", action="store_true",
        help="Show the classification records in human-readable form."
    )
    parser.add_argument(
        "text", nargs="*",
        help="Input text(s) to convert (e.g., cconv -t iso3 'Czech Republic')."
    )
    try:
        args = parser.parse_args()
        if args.info:
            result = cconv(json_file=args.source, info=True)
            _print_human_readable(result)
            return 0
        if args.dump:
            result = cconv(json_file=args.source, dump=True)
            _print_human_readable(result)
            return 0
        if not args.to:
            print("error: --to/-t is required unless using --info or --dump",
                  file=sys.stderr)
            return 1
    
        # if no positional args, try reading from stdin (one item per line)
        inputs = list(args.text)
        if not inputs and not sys.stdin.isatty():
            inputs = [line.strip() for line in sys.stdin if line.strip()]
        if not inputs:
            print("error: provide at least one input text (args or STDIN)",
                  file=sys.stderr)
            return 1

        # preserve shape: single token -> str, multiple -> list[str]
        text_in: str | list[str] = inputs[0] if len(inputs) == 1 else inputs
        result = cconv(json_file=args.source, to=args.to, text=text_in)
        if isinstance(result, list):
            for item in result:
                print(item)
        else:
            print(result)
        return 0
    except BrokenPipeError:
        try:
          sys.stdout.close()
        finally:
          return 0
    except KeyboardInterrupt:
          return 130

if __name__ == "__main__":
    sys.exit(main())
