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
    "SubmissionBaseView", "SubmissionList", "SubmissionCreate", "SubmissionDetail",
    "SubmissionUpdate", "SubmissionDelete"]
__author__ = "pmeier82"

Submission = apps.get_registered_model("djspikeval", "submission")


class SubmissionBaseView(object):
    model = Submission


class SubmissionList(SubmissionBaseView, ListView):
    template_name = "djspikeval/submission/list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            Submission.objects.all()
        else:
            return Submission.objects.filter(
                Q(status=Submission.STATUS.public) |
                Q(owner__pk=self.request.user.pk)
            )


class SubmissionCreate(SubmissionBaseView, CreateView):
    template_name = "djspikeval/submission/create.html"
    form_class = SubmissionForm

    def get_form_kwargs(self):
        kwargs = super(SubmissionCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class SubmissionDetail(SubmissionBaseView, DetailView):
    template_name = "djspikeval/submission/detail.html"


class SubmissionUpdate(SubmissionBaseView, UpdateView):
    template_name = "djspikeval/submission/update.html"
    form_class = SubmissionForm

    def get_form_kwargs(self):
        kwargs = super(SubmissionUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class SubmissionDelete(SubmissionBaseView, DeleteView):
    template_name = "djspikeval/submission/delete.html"
    success_url = reverse_lazy("submission:list")


if __name__ == "__main__":
    pass
