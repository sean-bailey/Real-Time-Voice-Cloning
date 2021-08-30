"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import distutils.text_file
from pathlib import Path
from typing import List

# Always prefer setuptools over distutils
import setuptools


def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()

keywords = [ 'pytorch','torch','tensorflow','machine learning','research',"voice cloning","real time voice cloning"]

setuptools.setup(
    name="voiceCloner",
    version="0.1.1",
    author="Sean Bailey",
    author_email="seanbailey518@gmail.com",
    description="This is a wrapper around the Real Time Voice Cloning project by @Corentinj (https://github.com/CorentinJ/Real-Time-Voice-Cloning)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sean-bailey/Real-Time-Voice-Cloning",
    keywords = keywords,
    install_requires=_parse_requirements('requirements.txt'),
    #install_requires=parse_requirements('requirements.txt', session='hack'),
    packages = setuptools.find_packages(),
    classifiers=['Development Status :: 4 - Beta',
              'Intended Audience :: End Users/Desktop',
              'Intended Audience :: Developers',
              'Intended Audience :: System Administrators',
              'License :: OSI Approved :: GNU AFFERO GENERAL PUBLIC LICENSE V3',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Topic :: Communications :: Email',
              'Topic :: Office/Business',
              'Topic :: Software Development :: Bug Tracking',
              ],
)
