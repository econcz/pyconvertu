import pkgutil

# ISO-3166-1 JSON file
pyconvertu_classification = pkgutil.get_data(__name__, r'classification.json')

from pyconvertu.pyconvertu import convert              # main function
from pyconvertu.pyconvertu import classification       # full classification
from pyconvertu.pyconvertu import info                 # info, metadata