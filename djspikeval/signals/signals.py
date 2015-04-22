# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.dispatch import Signal

__all__ = ["spike_analysis", "spike_validation_rd", "spike_validation_st"]
__author__ = "pmeier82"

spike_analysis = Signal()
spike_validation_rd = Signal()
spike_validation_st = Signal()

if __name__ == "__main__":
    pass
