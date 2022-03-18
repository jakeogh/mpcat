# -*- coding: utf-8 -*-


from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = ["click"]

config = {
    "version": "0.1",
    "name": "mpcat",
    "url": "https://github.com/jakeogh/mpcat",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "write messagepacked files to stdout unchanged if stdout is not a tty, otherwise, repr()",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"mpcat": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "mpcat=mpcat.mpcat:cli",
        ],
    },
}

setup(**config)
