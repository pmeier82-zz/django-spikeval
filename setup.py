# -*- coding: utf-8 -*-
#
# django-spikeval - setup.py
#
# Philipp Meier <pmeier82 at googlemail dot com>
# 2015-02-23
#

from setuptools import setup

VERSION = __import__("djspikeval").__version__

if __name__ == "__main__":
    setup(
        name="django-spikeval",
        version=VERSION,

        description="Spikesorting evaluation package for the G-Node spike project.",
        long_description=open("README.rst").read(),

        url="https://github.com/pmeier82/django-spikeval",
        license="BSD",
        author="Philipp Meier",
        author_email="pmeier82@gmail.com",

        install_requires=["django>=1.7", "django-taggit>=0.12", "SpikEval"],
        packages=["djspikeval"],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ])
