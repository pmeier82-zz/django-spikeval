# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import template
from django.db import models

register = template.Library()
Analysis = models.get_model('spike', 'analysis')
Dataset = models.get_model('spike', 'dataset')
Module = models.get_model('spike', 'module')
Result = models.get_model('spike', 'result')

##---FILTER

@register.filter
def sort(qset):
    try:
        return qset.order_by('id')
    except:
        return qset


##---TAGS

@register.inclusion_tag('../templates/result_base.html')
def render_results(ev, mod, **kwargs):
    """render tag for results of analysis for specific module"""

    assert isinstance(ev, Analysis), 'got ev: %s, expected %s' % (ev.__class__, Analysis)
    assert isinstance(mod, Module), 'got mod: %s, expected %s' % (mod.__class__, Module)

    tempalte_name = 'spike/module/%s/result.html' % mod.path
    res_list = Result.objects.filter(evaluation=ev, module=mod).select_subclasses()

    return {'template': tempalte_name, 'ev': ev, 'res_list': res_list}


@register.inclusion_tag('../templates/summary_base.html')
def render_summary(bm, mod, **kwargs):
    """render tag for summary of dataset for specific module"""

    assert isinstance(bm, Dataset), 'got ev: %s, expected %s' % (bm.__class__, Dataset)
    assert isinstance(mod, Module), 'got mod: %s, expected %s' % (mod.__class__, Module)

    tempalte_name = 'spike/module/%s/summary.html' % mod.path
    res_list = Result.objects.filter(evaluation__trial__benchmark=bm, module=mod).select_subclasses()

    return {'template': tempalte_name, 'bm': bm, 'mod': mod, 'res_list': res_list}

##---MAIN

if __name__ == '__main__':
    pass
