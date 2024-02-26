from setuptools import setup, find_packages
from glob import glob

setup(
    name="BrailleEd Software",
    version="0.1",
    packages=find_packages(),
    data_files=[("tables", glob("text_to_braille/tables/*"))],
)
