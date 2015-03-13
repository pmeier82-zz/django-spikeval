# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.dispatch import Signal

__all__ = ["spike_evaluation", "spike_validate_rd", "spike_validate_st"]
__author__ = "pmeier82"

spike_evaluation = Signal()
spike_validate_rd = Signal()
spike_validate_st = Signal()

if __name__ == "__main__":
    pass
