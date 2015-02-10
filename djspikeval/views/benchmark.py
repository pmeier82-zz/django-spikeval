# -*- coding: utf-8 -*-

import zipfile
from StringIO import StringIO

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils import importlib
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import nan, nansum, nanmax

from djspikeval.forms import BenchmarkForm, TrialForm, BatchSubmitForm, AttachmentForm
from djspikeval.util import render_to, PLOT_COLORS


__author__ = "pmeier82"

Benchmark = apps.get_registered_model("djspikeval", "benchmark")
Trial = apps.get_registered_model("djspikeval", "trial")
# Module = apps.get_registered_model('spike', 'module')

@render_to("djspikeval/benchmark/list.html")
def list__old(request):
    """renders a list of available benchmarks"""

    # post request
    if request.method == "POST":
        bm_form = BenchmarkForm(data=request.POST)
        if bm_form.is_valid():
            bm = bm_form.save(user=request.user)
            messages.success(request, 'Benchmark creation successful: "%s"' % bm.name)
            return redirect(bm)
        else:
            messages.error(request, 'Benchmark creation failed')

    # get request
    else:
        bm_form = BenchmarkForm()

    # benchmark list
    object_list = Benchmark.objects.filter(status=Benchmark.STATUS.public)
    if request.user.is_authenticated():
        if request.user.is_superuser:
            object_list = Benchmark.objects.all()

    # search_user
    scope = request.GET.get('scope', None)
    if scope is not None and request.user.is_authenticated():
        object_list = object_list.filter(owner=request.user)

    # search terms
    search_terms = request.GET.get('search', None)
    if search_terms:
        object_list = (
            object_list.filter(name__icontains=search_terms) |
            object_list.filter(description__icontains=search_terms) |
            object_list.filter(owner__username__icontains=search_terms))

    # response
    return {'bm_form': bm_form,
            'object_list': object_list,
            'search_terms': search_terms,
            'scope': scope is not None}


@render_to("djspikeval/benchmark/detail.html")
def detail__old(request, pk):
    """renders details of a particular benchmark"""

    # init and checks
    try:
        bm = Benchmark.objects.get(pk=pk)
        assert bm.is_accessible(request.user), 'insufficient permissions'
    except Exception, ex:
        messages.error(request, 'You are not allowed to view or modify this Benchmark: %s' % ex)
        return redirect('bm_list')
    bm_form = tr_form = bt_form = ap_form = None
    tr_list = bm.trial_set.order_by('parameter')
    if not bm.is_accessible(request.user):
        tr_list = filter(lambda x: x.is_valid, tr_list)

    # post request
    if request.method == 'POST':
        if bm.is_accessible(request.user):
            if 'benchmark:edit' in request.POST:
                bm_form = BenchmarkForm(data=request.POST, instance=bm)
                if bm_form.is_valid():
                    bm = bm_form.save()
                    messages.success(request, 'Benchmark edit successful!')
                    # return redirect(bm)
                else:
                    messages.error(request, 'Benchmark edit failed!')
            elif 'tr_create' in request.POST:
                tr_form = TrialForm(benchmark=bm, data=request.POST, files=request.FILES)
                tr = None
                if tr_form.is_valid():
                    tr = tr_form.save()
                if tr is not None:
                    tr.validate()
                    messages.success(request, 'Trial creation successful: "%s"' % tr)
                    return redirect(tr)
                else:
                    messages.error(request, 'Trial creation failed')
            elif 'ap_create' in request.POST:
                ap_form = AttachmentForm(data=request.POST, files=request.FILES, obj=bm)
                if ap_form.is_valid():
                    ap = ap_form.save()
                    messages.success(request, 'Appendix creation successful: "%s"' % ap)
                else:
                    messages.error(request, 'Appendix creation failed!')

        # user submission
        if 'ev_submit' in request.POST:
            bt_form = BatchSubmitForm(data=request.POST, files=request.FILES, benchmark=bm)
            if bt_form.is_valid():
                ev = bt_form.save(user=request.user)
                messages.success(request, 'Evaluation submission successful')
                return redirect(ev)
            else:
                messages.error(request, 'Evaluation submission failed')

    # build forms
    if not ap_form:
        ap_form = AttachmentForm(obj=bm)
    if not bm_form:
        bm_form = BenchmarkForm(instance=bm)
    if not tr_form:
        tr_form = TrialForm(benchmark=bm)
    if not bt_form:
        bt_form = BatchSubmitForm(benchmark=bm)

    # response
    return {'bm': bm,
            'appendix': bm.data_set.filter(kind='appendix'),
            'tr_list': tr_list,
            'ap_form': ap_form,
            'bm_form': bm_form,
            'bt_form': bt_form,
            'tr_form': tr_form}


@login_required
def toggle__old(request, pk):
    """toggle status for benchmark"""

    try:
        bm = Benchmark.objects.get(pk=pk)
        assert bm.is_accessible(request.user), 'insufficient permissions'
        bm.toggle()
        messages.info(request, 'Benchmark "%s" toggled to %s' % (bm, bm.status))
    except Exception, ex:
        messages.error(request, 'Benchmark not toggled: %s' % ex)
    finally:
        return redirect(bm)


@login_required
def delete(request, pk):
    """delete benchmark"""

    try:
        bm = Benchmark.objects.get(pk=pk)
        assert bm.is_accessible(request.user), 'insufficient permissions'
        Benchmark.objects.get(pk=pk).delete()
        messages.success(request, 'Benchmark "%s" deleted' % bm)
    except Exception, ex:
        messages.error(request, 'Benchmark not deleted: %s' % ex)
    finally:
        return redirect('bm_list')


@render_to("djspikeval/benchmark/summary.html")
def summary__old(request, pk):
    """summary page for benchmark"""

    try:
        bm = Benchmark.objects.get(pk=pk)
        assert bm.is_accessible(request.user), 'insufficient permissions'
    except Exception, ex:
        messages.error(request, 'You are not allowed to view or modify this Benchmark: %s' % ex)
        return redirect('bm_list')
    bt_list = bm.batch_set.filter(status=Benchmark.STATUS.public)
    if request.user.is_authenticated():
        bt_list_self = bm.batch_set.filter(status=Benchmark.STATUS.private)
        if not request.user.is_superuser:
            bt_list_self = bt_list_self.filter(owner=request.user)
        bt_list |= bt_list_self
    mod_list = bm.module_set.filter(enabled=True)
    for mod in mod_list:
        keep = False
        try:
            module_pkg = importlib.import_module('spike.module.%s' % mod.path)
            keep = module_pkg.__has_summary__
        except:
            pass
        finally:
            if keep is False:
                mod_list = mod_list.exclude(id=mod.id)

    # TODO: order by clause for modules
    return {'bm': bm,
            'bt_list': bt_list.order_by('id'),
            'mod_list': mod_list}


def summary_plot__old(request, bm_pk=None, mod_pk=None, mode=None, legend=False):
    """generate a plot of the benchmark summary"""

    ## DEBUG
    print 'bm_pk :: %s(%s)' % (bm_pk.__class__.__name__, bm_pk)
    print 'mod_pk :: %s(%s)' % (mod_pk.__class__.__name__, mod_pk)
    print 'mode :: %s(%s)' % (mode.__class__.__name__, mode)
    print 'legend :: %s(%s)' % (legend.__class__.__name__, legend)
    ## GUBED

    fig = None
    try:
        # init and checks
        bm = get_object_or_404(Benchmark.objects.all(), id=bm_pk)
        tr_list = bm.trial_set.order_by('parameter')
        bt_list = bm.batch_set.filter(status=Benchmark.STATUS.public)
        if request.user.is_authenticated():
            eb_list_self = bm.batch_set.filter(status=Benchmark.STATUS.private)
            if not request.user.is_superuser:
                eb_list_self = eb_list_self.filter(owner=request.user)
            bt_list |= eb_list_self
        bt_list.order_by('id')
        param_labels = [t.parameter for t in tr_list]
        np = len(param_labels)
        y_max = 1.

        # build figure
        fig = Figure(
            figsize=(5, 5),
            facecolor='white',
            edgecolor='white',
            frameon=False)
        # ax = fig.add_subplot(111)
        ax = fig.add_axes([.15, .1, .8, .8])
        ax.set_color_cycle(PLOT_COLORS)

        # plot data
        if mode is None or (mode is not None and mode not in ['error_sum',
                                                              'FPAEno',
                                                              'FNno',
                                                              'FP',
                                                              'FPAEo',
                                                              'FNo']):
            mode = 'error_sum'
        for bt in bt_list:
            y_curve = [nan] * np
            for ev in bt.evaluation_set.all():
                try:
                    y_curve[tr_list.index(ev.trial)] = ev.summary_table()[mode]
                except:
                    pass
            if nansum(y_curve) >= 0:
                # TODO: fix "empty" evaluation batches!!
                y_max = nanmax(y_curve + [y_max])
                # y_curve = map(lambda x: x + 1.0, y_curve)
                # ax.semilogy(y_curve, 'o-', label='EB #%s' % eb.id)
                ax.plot(y_curve, 'o-', label='EB #%s' % bt.id)

        # beautify Y-axis
        ax.set_ylabel('Error Count')
        y_margin = y_max * 0.05
        ax.set_ylim(-y_margin, y_max + y_margin)
        # beautify X-axis
        ax.set_xlabel(bm.parameter)
        x_margin = np * 0.05
        ax.set_xlim(-x_margin, (1 + .5 * (legend is True)) * np + x_margin - 1)
        ax.set_xticks(range(np))
        ax.set_xticklabels(param_labels)
        # figure title
        title = {
            'error_sum': 'Total Error',
            'FPAEno': 'Classification Error (NO)',
            'FNno': 'False Negative (NO)',
            'FP': 'False Positive (NO)',
            'FPAEo': 'Classification Error (O)',
            'FNo': 'False Negative (O)',
        }.get(mode, 'Total Error')
        ax.set_title(title)
        if legend is True:
            ax.legend(
                loc='upper center',
                ncol=2,
                fancybox=True,
                bbox_to_anchor=(.90, 1),
                numpoints=1,
                prop={'size': 8},
            )
        ax.grid()

        ## DEBUG
        # print 'DPI:', fig.get_dpi(), 'y_max', y_max
        ## GUBED
    except:
        import sys, traceback

        traceback.print_exception(*sys.exc_info())
        sys.exc_clear()
    finally:
        # response = HttpResponse(content_type='image/png')
        response = HttpResponse(content_type='image/svg+xml')
        try:
            canvas = FigureCanvas(fig)
            # canvas.print_png(response)
            canvas.print_svg(response)
        except:
            pass
        return response


def download__old(request, pk):
    # init and checks
    try:
        bm = Benchmark.objects.get(pk=pk)
        assert bm.is_accessible(request.user), 'insufficient permissions'
    except Exception, ex:
        messages.error(request, 'You are not allowed to view or modify this Benchmark: %s' % ex)
        return redirect('bm_list')
    tr_list = [tr for tr in bm.trial_set.order_by('parameter') if tr.is_valid]
    arc, buf = None, None

    # build archive
    try:
        # build buffer and archive
        buf = StringIO()
        arc = zipfile.ZipFile(buf, mode='w')
        for tr in tr_list:
            arc.writestr(tr.rd_file.name, tr.rd_file.file.read())
            if tr.gt_file and tr.gt_public:
                arc.writestr(tr.gt_file.name, tr.gt_file.file.read())
        arc.close()
        buf.seek(0)

        response = HttpResponse(buf.read())
        response['Content-Disposition'] = 'attachment; filename=%s.zip' % slugify(bm.name)
        response['Content-Type'] = 'application/x-zip'
        return response
    except Exception, ex:
        messages.error(request, 'Error creating archive: %s' % ex)
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


# CLASS BASED VIEWS

class BenchmarkBaseView(object):
    model = Benchmark


class BenchmarkList(BenchmarkBaseView, ListView):
    template_name = "djspikeval/benchmark/list.html"


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
            bm = Benchmark.objects.get(pk=pk)
            assert bm.is_accessible(request.user), 'insufficient permissions'
        except Exception, ex:
            messages.error(request, 'You are not allowed to view or modify this Benchmark: %s' % ex)
            return redirect('bm_list')
        tr_list = [tr for tr in bm.trial_set.order_by('parameter') if tr.is_valid]
        arc, buf = None, None

        # build archive
        try:
            # build buffer and archive
            buf = StringIO()
            arc = zipfile.ZipFile(buf, mode='w')
            for tr in tr_list:
                arc.writestr(tr.rd_file.name, tr.rd_file.file.read())
                if tr.gt_file and tr.gt_public:
                    arc.writestr(tr.gt_file.name, tr.gt_file.file.read())
            arc.close()
            buf.seek(0)

            response = HttpResponse(buf.read())
            response['Content-Disposition'] = 'attachment; filename=%s.zip' % slugify(bm.name)
            response['Content-Type'] = 'application/x-zip'
            return response
        except Exception, ex:
            messages.error(request, 'Error creating archive: %s' % ex)
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
    """summary for this benchmark"""

    def get(self, request, *args, **kwargs):
        try:
            obj = Benchmark.objects.get(pk=self.kwargs["pk"])
            assert obj.is_accessible(request.user), "insufficient permissions"
            obj.toggle()
            messages.info(request, "Benchmark \"%s\" toggled to %s" % (obj, obj.status))
        except Exception, ex:
            messages.error(request, "Benchmark not toggled: %s" % ex)
        finally:
            return redirect(obj)


if __name__ == "__main__":
    pass
