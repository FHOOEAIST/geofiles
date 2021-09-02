import pathlib

import pkg_resources
from setuptools import setup

try:
    with pathlib.Path('requirements.txt').open() as requirements_txt:
        install_requires = [
            str(requirement)
            for requirement
            in pkg_resources.parse_requirements(requirements_txt)
        ]
except FileNotFoundError:
    install_requires = []

setup(
    package_dir={"": "src"},
    install_requires=install_requires,
)
