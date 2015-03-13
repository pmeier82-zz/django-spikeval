# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import apps
from django.conf import settings
from django.db import models
from django.conf import settings
from django.utils import importlib
from celery.task import task
from datetime import datetime
from StringIO import StringIO

from spikeval.datafiles import read_gdf_sts, read_hdf5_arc
from spikeval.log import Logger

from ..signals import spike_evaluation

Analysis = apps.get_registered_model("djspikeval", "analysis")
Module = apps.get_registered_model("djspikeval", "module")

__all__ = ["run_modules_for_evaluation"]
__author__ = "pmeier82"

USE_CELERY = getattr(settings, "USE_CELERY", False)
if getattr(settings, "CELERY_USE_PRIORITY", None) is not None:
    USE_CELERY = getattr(settings, "CELERY_USE_PRIORITY")


def run_modules_for_evaluation(sender, **kwargs):
    if getattr(settings, "DEBUG", None) is True:
        print "starting analysis [class: %s::%s]" % (sender.__class__.__name__, sender.id)
    if USE_CELERY:
        task_run_modules.delay(sender)
    else:
        task_run_modules(sender)


spike_evaluation.connect(run_modules_for_evaluation, dispatch_uid=__file__)


@task
def task_run_modules(pk, **kwargs):
    """run all enabled modules for an analysis

    :type pk: Analysis
    :param pk: Analysis entity
    :keyword: any, will be passed to modules as parameters

    :returns: True on success, False on error
    """

    success = None
    logger = Logger.get_logger(StringIO())
    try:
        obj = Analysis.objects.get(pk=pk)
        obj.status = Analysis.STATUS.running
        obj.save()
        mod_list = obj.datafile.dataset.module_set.all()
    except:
        success = False
    else:
        try:
            logger.log_delimiter_line()

            rd_file = obj.datafile.rd_file
            gt_file = obj.datafile.gt_file
            st_file = obj.st_file
            logger.log("processing: %s" % obj)

            logger.log("reading input files")
            rd, sampling_rate = read_hdf5_arc(rd_file.data.path)
            if sampling_rate is not None:
                kwargs.update(sampling_rate=sampling_rate)
            ev_sts = read_gdf_sts(st_file.file.path)
            gt_sts = read_gdf_sts(gt_file.file.path)
            logger.log("done reading input files")

            logger.log_delimiter_line()

            # modules
            assert len(mod_list), "Module list is empty!"
            for mod in mod_list:
                logger.log("starting module: %s" % mod)
                module_pkg = importlib.import_module("djspikeval.module.{}".format(mod.path))
                _tick_ = datetime.now()
                module = module_pkg.module_cls(rd, gt_sts, ev_sts, logger, **kwargs)
                module.apply()
                module.save(mod, obj)
                _tock_ = datetime.now()
                logger.log("finished: {}".format(str(_tock_ - _tick_)))
                logger.log_delimiter_line()
                del module, module_pkg
        except Exception, ex:
            logger.log("ERROR: (%s) %s" % (ex.__class__.__name__, str(ex)))
            success = False
            obj.status = Analysis.STATUS.failure
        else:
            success = True
            obj.status = Analysis.STATUS.success
        finally:
            obj.task_log = logger.get_content()
            obj.save()
            print obj.task_log
    finally:
        return success


if __name__ == "__main__":
    pass
