# -*- coding: utf-8 -*-

from django.dispatch import Signal

__all__ = ["spike_evaluation_run", "spike_validate_rd", "spike_validate_st"]
__author__ = "pmeier82"

spike_evaluation_run = Signal()
spike_validate_rd = Signal()
spike_validate_st = Signal()

if __name__ == "__main__":
    pass
