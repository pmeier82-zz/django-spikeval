# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
from StringIO import StringIO

from django.apps import apps
from django.conf import settings
from django.utils import importlib
from celery.task import task

from spikeval.datafiles import read_gdf_sts, read_hdf5_arc
from spikeval.log import Logger
from ..signals import spike_analysis


Analysis = apps.get_registered_model("djspikeval", "analysis")
Module = apps.get_registered_model("djspikeval", "module")

__all__ = ["run_modules_for_analysis"]
__author__ = "pmeier82"

USE_CELERY = getattr(settings, "USE_CELERY", False)
if getattr(settings, "CELERY_USE_PRIORITY", None) is not None:
    USE_CELERY = getattr(settings, "CELERY_USE_PRIORITY")


def run_modules_for_analysis(sender, **kwargs):
    if getattr(settings, "DEBUG", None) is True:
        print "starting analysis [class: %s::%s]" % (sender.__class__.__name__, sender.id)
    if USE_CELERY:
        task_run_modules.delay(sender)
    else:
        task_run_modules(sender)


spike_analysis.connect(run_modules_for_analysis, dispatch_uid=__file__)


@task
def task_run_modules(ana_pk, **kwargs):
    """run all enabled modules for an analysis

    :type ana_pk: Analysis
    :param ana_pk: Analysis entity
    :keyword: any, will be passed to modules as parameters

    :returns: True on success, False on error
    """

    ana = None
    success = None
    logger = Logger.get_logger(StringIO(""))
    try:
        # get analysis
        ana = Analysis.objects.get(pk=ana_pk.pk)
        logger.log_delimiter_line()
        logger.log("processing %s" % ana)
        ana.status = Analysis.STATUS.running
        ana.save()

        # get module list
        mod_list = ana.datafile.dataset.module_set.all()
        assert mod_list, "module list is empty!"

        # get file handles
        logger.log("reading input files")
        rd_file = ana.datafile.rd_file
        gt_file = ana.datafile.gt_file
        st_file = ana.st_file
        rd, sampling_rate = read_hdf5_arc(rd_file.data.path)
        if sampling_rate is not None:
            kwargs.update(sampling_rate=sampling_rate)
        ev_sts = read_gdf_sts(st_file.data.path)
        gt_sts = read_gdf_sts(gt_file.data.path)
        logger.log("done reading input files")

        # apply modules
        _tick_all = datetime.now()
        for mod in mod_list:
            logger.log_delimiter_line()
            logger.log("starting {}".format(mod))
            module_cls = mod.get_module_cls()
            _tick_ = datetime.now()
            module = module_cls(rd, gt_sts, ev_sts, logger, **kwargs)
            module.apply()
            module.save(mod, ana)
            _tock_ = datetime.now()
            logger.log("finished in {}".format(str(_tock_ - _tick_)))
            del module, module_cls, _tick_, _tock_
        _tock_all = datetime.now()
        logger.log_delimiter_line()
        logger.log("finished all module in {}".format(str(_tock_all - _tick_all)))
    except Exception, ex:
        logger.log_delimiter_line()
        logger.log("ERROR ({}) :: {}".format(ex.__class__.__name__, ex))
        success = False
    else:
        success = True
    finally:
        log_cnt = logger.get_content()
        if ana:
            if success is True:
                ana.status = Analysis.STATUS.success
            else:
                ana.status = Analysis.STATUS.failure
            ana.task_log = log_cnt
            ana.save()
        print log_cnt
        return success


if __name__ == "__main__":
    pass
