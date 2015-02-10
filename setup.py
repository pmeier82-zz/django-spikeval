## -*- coding: utf-8 -*-

from setuptools import setup

version = __import__("djspikeval").__version__

## MAIN

if __name__ == "__main__":
    setup(
        name="django-spikeval",
        version=version,

        description="Spikesorting evaluation package for the G-Node spike project.",
        long_description=open("README.rst").read(),

        url="https://github.com/pmeier82/django-spikeval",
        license="BSD",
        author="Philipp Meier",
        author_email="pmeier82@gmail.com",

        install_requires=["django>=1.7", "django-taggit>=0.12"],
        packages=["djspikeval"],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ])
