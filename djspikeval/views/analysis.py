# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import simplejson
import zipfile
from StringIO import StringIO

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils import importlib
from django.views.generic import (
    View, DetailView, UpdateView, DeleteView, CreateView, ListView, RedirectView)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import nan, nansum, nanmax

from djspikeval.forms import SubmissionForm
# from djspikeval.util import render_to, PLOT_COLORS

__all__ = [
    "AnalysisBaseView", "AnalysisList", "AnalysisCreate", "AnalysisDetail", "AnalysisUpdate", "AnalysisDelete",
    "AnalysisDownload", "SubmissionToggle", "SubmissionStart", "AnalysisStart"]
__author__ = "pmeier82"

Analysis = apps.get_registered_model("djspikeval", "analysis")
Dataset = apps.get_registered_model("djspikeval", "dataset")
Submission = apps.get_registered_model("djspikeval", "submission")


class AnalysisBaseView(object):
    model = Submission


class AnalysisList(AnalysisBaseView, ListView):
    template_name = "djspikeval/analysis/list.html"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Submission.objects.all()
        else:
            return Submission.objects.filter(
                Q(status=Submission.STATUS.public) |
                Q(user__pk=self.request.user.pk)
            )


class AnalysisCreate(AnalysisBaseView, CreateView):
    template_name = "djspikeval/analysis/create.html"
    form_class = SubmissionForm

    def get_form_kwargs(self):
        kwargs = super(AnalysisCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["dataset"] = Dataset.objects.get(pk=self.kwargs["pk"])
        return kwargs


class AnalysisDetail(AnalysisBaseView, DetailView):
    template_name = "djspikeval/analysis/detail.html"


class AnalysisUpdate(AnalysisBaseView, UpdateView):
    template_name = "djspikeval/analysis/update.html"
    form_class = SubmissionForm

    def get_form_kwargs(self):
        kwargs = super(AnalysisUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AnalysisDelete(AnalysisBaseView, DeleteView):
    template_name = "djspikeval/analysis/delete.html"
    success_url = reverse_lazy("analysis:list")


class AnalysisDownload(AnalysisBaseView, View):
    """serve submission as archive"""

    def get(self, request, *args, **kwargs):
        try:
            1 / 0
        except Exception, ex:
            messages.error(request, "You are not allowed to view or modify this Analysis: %s" % ex)
            return redirect("analysis:list")


class SubmissionToggle(AnalysisBaseView, View):
    """toggle submission visibility"""

    def get(self, request, *args, **kwargs):
        try:
            obj = get_object_or_404(Submission, pk=self.kwargs["pk"])
            assert obj.is_accessible(self.request.user), "insufficient permissions"
            assert obj.dataset.is_public(), "cannot disclose analysis for undisclosed dataset!"
            obj.toggle()
            messages.info(self.request, "Analysis \"{}\" toggled to {}".format(obj.id, obj.status))
        except Exception, ex:
            messages.error(self.request, "Analysis not toggled: {}".format(ex))
            obj = "analysis:list"
        finally:
            return redirect(obj)


class SubmissionStart(AnalysisBaseView, View):
    """start analysis of the whole submission"""

    def get(self, request, *args, **kwargs):
        try:
            obj = get_object_or_404(Submission, pk=self.kwargs["pk"])
            assert obj.is_accessible(self.request.user), "insufficient permissions"
            for ana in obj.analysis_set.all():
                ana.start()
            messages.info(self.request, "Analyses started!")
        except Exception, ex:
            messages.error(self.request, "Analyses not restarted: %s" % ex)
            obj = "analysis:list"
        finally:
            return redirect(obj)


class AnalysisStart(AnalysisBaseView, View):
    """start analysis of a single analysis"""

    def get(self, request, *args, **kwargs):
        try:
            obj = get_object_or_404(Analysis, pk=self.kwargs["pk"])
            assert obj.is_accessible(self.request.user), "insufficient permissions"
            obj.start()
            messages.info(self.request, "Analysis started!")
        except Exception, ex:
            messages.error(self.request, "Analysis not started: %s" % ex)
            obj = "analysis:list"
        finally:
            return redirect(obj.submission)


if __name__ == "__main__":
    pass
