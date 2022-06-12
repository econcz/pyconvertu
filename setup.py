from distutils.core import setup
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# setup function
setup(
    name = 'pyconvertu',
    packages = ['pyconvertu'],
    version = '0.4.0',
    license = 'MIT',
    description = 'Tools for creation or conversion of lists from/to desired classification (the default is ISO 3166-1)',
    long_description=long_description,
    include_package_data = True,
    package_data={"": ["*.json"],},
    author = 'econcz',
    author_email = '29724411+econcz@users.noreply.github.com',
    url = 'https://github.com/econcz/pyconvertu',
    download_url = 'https://github.com/econcz/pyconvertu/archive/pypi-0_4_0.tar.gz',
    keywords = [
        'pycountry-convert', 'pycountry', 'conversion', 'tune',
        'ISO-3166', 'alpha-2', 'alpha-3', 'numeric', 'English', 'French',
        'regular expressions', "classification", "text"
    ],
    install_requires = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Filters',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
  ],
)
