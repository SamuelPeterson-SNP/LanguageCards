import setuptools
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="LanguageDeck",
    version="0.0.1",
    author="Samuel Peterson",
    author_email="sam.houston.peterson@gmail.com",
    licence="BSD 2-Clause",
    packages=setuptools.find_packages(),
    install_requires=["sqlalchemy>=1.1"],
    keywords="education foreign language flash cards"
)
