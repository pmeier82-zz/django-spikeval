# -*- coding: utf-8 -*-

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

from djspikeval.forms import BenchmarkForm, BenchmarkSearchForm
# from djspikeval.util import render_to, PLOT_COLORS

__all__ = [
    "BenchmarkBaseView", "BenchmarkList", "BenchmarkCreate", "BenchmarkDetail",
    "BenchmarkUpdate", "BenchmarkDelete", "BenchmarkDownload", "BenchmarkSummary",
    "BenchmarkToggle"]
__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "benchmark")


class BenchmarkBaseView(object):
    model = Benchmark


class BenchmarkList(BenchmarkBaseView, ListView):
    template_name = "djspikeval/benchmark/list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Benchmark.objects.all()
        else:
            return Benchmark.objects.filter(
                Q(status=Benchmark.STATUS.public) |
                Q(owner__pk=self.request.user.pk)
            )


class BenchmarkCreate(BenchmarkBaseView, CreateView):
    template_name = "djspikeval/benchmark/create.html"
    form_class = BenchmarkForm

    def get_form_kwargs(self):
        kwargs = super(BenchmarkCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class BenchmarkDetail(BenchmarkBaseView, DetailView):
    template_name = "djspikeval/benchmark/detail.html"


class BenchmarkUpdate(BenchmarkBaseView, UpdateView):
    template_name = "djspikeval/benchmark/update.html"
    form_class = BenchmarkForm

    def get_form_kwargs(self):
        kwargs = super(BenchmarkUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class BenchmarkDelete(BenchmarkBaseView, DeleteView):
    template_name = "djspikeval/benchmark/delete.html"
    success_url = reverse_lazy("benchmark:list")


class BenchmarkDownload(BenchmarkBaseView, View):
    """serve benchmark as archive"""

    def get(self, request, *args, **kwargs):
        try:
            bm = get_object_or_404(Benchmark, pk=self.kwargs["pk"])
            assert bm.is_accessible(request.user), "insufficient permissions"
        except Exception, ex:
            messages.error(request, "You are not allowed to view or modify this Benchmark: %s" % ex)
            return redirect("benchmark:list")
        tr_list = [tr for tr in bm.trial_set.order_by("parameter") if tr.is_valid]
        arc, buf = None, None

        # build archive
        try:
            # build buffer and archive
            buf = StringIO()
            arc = zipfile.ZipFile(buf, mode='w')
            for tr in tr_list:
                arc.writestr(tr.rd_file.name, tr.rd_file.data.read())
                if tr.gt_file and tr.gt_public:
                    arc.writestr(tr.gt_file.name, tr.gt_file.data.read())
            arc.close()
            buf.seek(0)

            response = HttpResponse(buf.read())
            response["Content-Disposition"] = "attachment; filename=%s.zip" % slugify(bm.name)
            response["Content-Type"] = "application/x-zip"
            return response
        except Exception, ex:
            messages.error(request, "Error creating archive: %s" % ex)
            return redirect(bm)
        finally:
            try:
                del arc
            except:
                pass
            try:
                del buf
            except:
                pass


class BenchmarkSummary(BenchmarkBaseView, View):
    """summary for this benchmark"""

    def get(self, request, *args, **kwargs):
        return HttpResponse("TEST")


class BenchmarkToggle(BenchmarkBaseView, View):
    """toggle benchmark visibility"""

    def get(self, request, *args, **kwargs):
        try:
            obj = get_object_or_404(Benchmark, pk=self.kwargs["pk"])
            assert obj.is_accessible(self.request.user), "insufficient permissions"
            obj.toggle()
            messages.info(self.request,
                          "Benchmark \"%s\" toggled to %s" % (obj, obj.status))
        except Exception, ex:
            messages.error(self.request, "Benchmark not toggled: %s" % ex)
        finally:
            return redirect(obj)


if __name__ == "__main__":
    pass
