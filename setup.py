# coding: utf-8

"""
:copyright: (c) 2014 by Taehoon Kim.
:license: BSD, see LICENSE for more details.

このライブラリはTaehoon Kim氏が開発し、Sh1maが改良したライブラリです。
"""

from distutils.core import setup

setup(
    name         = "line",
    version      = "1.0.0",
    author       = "Sh1ma",
    author_email = "in9lude@gmail.com",
    packages     = ["LineThrift", "line"],
    package_dir  = {"": "src"},
    install_requires = [
    "requests",
    "rsa",
    "simplejson",
    ]
)

