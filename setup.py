from distutils.core import setup
from os import path

# read the contents of README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, r'README'), encoding='utf-8') as f:
    readme_text = f.read()

# setup function
setup(
    name = 'pyconvertu',
    packages = ['pyconvertu'],
    version = '0.3.9',
    license = 'MIT',
    description = 'Tools for creation or conversion of lists from/to desired classification (the default is ISO 3166-1)',
    long_description=readme_text,
    include_package_data = True,
    package_data={"": ["*.json"],},
    author = 'econcz',
    author_email = '29724411+econcz@users.noreply.github.com',
    url = 'https://github.com/econcz/pyconvertu',
    download_url = 'https://github.com/econcz/pyconvertu/archive/pypi-0_3_9.tar.gz',
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
