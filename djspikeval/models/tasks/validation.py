# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import apps
from django.conf import settings
from celery.task import task
import scipy as sp
from StringIO import StringIO

from spikeval.datafiles import read_gdf_sts, read_hdf5_arc
from spikeval.log import Logger

from ..signals import spike_validate_st, spike_validate_rd

__all__ = ["spike_validate_rd", "spike_validate_st"]
__author__ = "pmeier82"

USE_CELERY = getattr(settings, "USE_CELERY", False)
if getattr(settings, "CELERY_USE_PRIORITY", None) is not None:
    USE_CELERY = getattr(settings, "CELERY_USE_PRIORITY")

Asset = apps.get_registered_model("base", "asset")


def validate_rawdata_file(sender, **kwargs):
    if USE_CELERY:
        task_validate_rawdata_file.delay(sender.rd_file.id)
    else:
        task_validate_rawdata_file(sender.rd_file.id)


spike_validate_rd.connect(validate_rawdata_file, dispatch_uid=__file__)


def validate_spiketrain_file(sender, **kwargs):
    if USE_CELERY:
        task_validate_spiketrain_file.delay(sender.gt_file.id)
    else:
        task_validate_spiketrain_file(sender.gt_file.id)


spike_validate_st.connect(validate_spiketrain_file, dispatch_uid=__file__)

# TASKS

# +Interface 1: The user uploads a file pair. The frontend calls a
# backend function with the following inputs:
# int Key - identifier for the dataset upload
#
# the backend will use the key to instantiate an object with which it
# can access the uploaded files. The files will be opened and checked
# for the content and return a boolean if the check was successful and a
# string containing information about the check like errors.
#
# This check function could look like:
#
# function checkenchmark(key)
# import Record
# datafile = Record.get(id = key)
#
# gtfilepath = datafile.groundtruth.path
# rawfilepath = datafile.raw_data.path
#
# [then check the files ... (gtfilepath, rawfilepath)]
#
# datafile.verfied = boolean
# recrod.verified_error = "string"
#
# return


@task
def task_validate_rawdata_file(pk, **kwargs):
    """validates rawdata file - that is an archive holding voltage traces from
    extracellular recordings to be a data to be analysed with spike sorting methods

    :type pk: int
    :param pk: pk of `Asset` entity

    :returns: bool -- True if file validates, False else. Processing
    log, including errors, will be written to the `Datafile` entity.
    """

    # init and checks
    valid = False
    logger = Logger.get_logger(StringIO())
    try:
        obj = Asset.objects.get(id=pk)
        assert obj.kind == "rd_file"
        df = obj.content_object
    except:
        logger.log("ERROR")
        return valid

    try:
        logger.log("looking at raw data file with pk: %s" % pk)
        rd, sr = read_hdf5_arc(obj.data.path)
        logger.log("found rd_file: %s" % obj.name)
        len_rd_sec = rd.shape[0] / sr
        logger.log("found data in %d channels, for %d sec" % (rd.shape[1], len_rd_sec))

        # TODO: more checks?

        logger.log("rd_file passed all checks")
        valid = True
    except Exception, ex:
        logger.log("ERROR: rawdata file check: %s" % str(ex))
    finally:
        df.valid_rd_log = logger.get_content()
        df.save()
        return valid


@task
def task_validate_spiketrain_file(pk, **kwargs):
    """validate spike train file - that is a text file in gdf format (space separated, 2col, [key,time])

    :type pk: int
    :param pk: pk of `Datafile` entity

    :returns: bool -- True if file validates, False else. Processing
    log, including errors, will be written to the `Datafile` entity.
    """

    # init and checks
    valid = False
    logger = Logger.get_logger(StringIO())
    try:
        obj = Asset.objects.get(id=pk)
        assert obj.kind == "st_file"
        df = obj.content_object
    except:
        logger.log("ERROR")
        return valid

    try:
        logger.log("looking at spike train file with pk: %s" % obj.id)
        sts = read_gdf_sts(obj.data.path)
        logger.log("found st_file: %s" % obj.name)
        for st in sts:
            if not isinstance(sts[st], sp.ndarray):
                raise TypeError("spike train %s not ndarray" % st)
            if not sts[st].ndim == 1:
                raise ValueError("spike trains have to be ndim==1")

        # TODO: more checks?

        logger.log("st_file passed all checks")
        valid = True
    except Exception, ex:
        logger.log('ERROR: spike train file check: %s' % str(ex))
    finally:
        obj.save()
        df.valid_gt_log = logger.get_content()
        df.save()
        return valid


if __name__ == '__main__':
    pass
