# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
from django.db import models

# PACKAGE
__author__ = "pmeier82"
__version__ = "0.1"
__module__ = "default visual"
__module_path__ = os.path.split(os.path.split(__file__)[0])[1]
__has_summary__ = False

# INIT
module = None
Module = None
try:
    Module = models.get_model("djspikeval", "module")
    module, created = Module.objects.get_or_create(
        name=__module__.title(),
        version=__version__,
        path=__module_path__)
    if created is True:
        print "just create module for:", __module__
        desc = "no description"
        try:
            desc = open("readme.txt", 'r').read()
        except:
            pass
        finally:
            module.description = desc
            module.save()
except Exception, ex:
    print "could not load module:", __module__, "\nerror:", ex
finally:
    del os, models, Module, module

from .module import Module as module_cls
