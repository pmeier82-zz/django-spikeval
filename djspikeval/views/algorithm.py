# -*- coding: utf-8 -*-

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from djspikeval.forms import AlgorithmForm
from djspikeval.util import render_to


__author__ = "pmeier82"

Algorithm = apps.get_registered_model("djspikeval", "algorithm")


@render_to("djspikeval/algorithm/list.html")
def list(request):
    """renders a list of available algorithms"""

    # init and checks
    object_list = Algorithm.objects.all()
    form = None

    # post request
    if request.method == 'POST':
        if request.POST.get("action", None) == "algorithm:create":
            form = AlgorithmForm(data=request.POST)
            if form.is_valid():
                obj = form.save(user=request.user)
                messages.success(request, "Algorithm creation successful")
                return redirect(obj)
            else:
                messages.error(request, "Algorithm creation failed")

    # search terms
    search_terms = request.GET.get("search", "")
    if search_terms:
        object_list = (
            object_list.filter(name__icontains=search_terms) |
            object_list.filter(owner__username__icontains=search_terms))

    # response
    return {
        "object_list": object_list,
        "form": form or AlgorithmForm(initial={"owner": request.user}),
        "search_terms": search_terms}


@render_to("djspikeval/algorithm/detail.html")
def detail(request, pk):
    """renders details for a particular algorithm"""

    # init and checks
    try:
        obj = Algorithm.objects.get(pk=pk)
    except Exception, ex:
        messages.error(request, "You are not allowed to view or modify this Algorithm: %s" % ex)
        return redirect("al_list")
    obj_form = None
    # ap_form = None

    # post request
    if request.method == "POST":
        if request.POST.get("action", None) == "algorithm:edit":
            obj_form = AlgorithmForm(data=request.POST, instance=obj)
            if obj_form.is_valid():
                obj = obj_form.save()
                messages.success(request, "Algorithm edit successful")
            else:
                messages.error(request, "Algorithm edit failed")

                # elif request.POST.get("action", None) == "appendix_create" in request.POST:
                # ap_form = AppendixForm(data=request.POST, files=request.FILES, obj=obj)
                # if ap_form.is_valid():
                # ap = ap_form.save()
                # messages.success(request, "Appendix creation successful: \"%s\"" % ap)
                # else:
                # messages.error(request, "Appendix creation failed")

    # response
    return {"obj": obj,
            "obj_form": obj_form or AlgorithmForm(instance=obj),
            # 'ap_form': ap_form or AppendixForm(obj=obj),
    }


@login_required
def delete(request, pk):
    """delete algorithm"""

    try:
        al = Algorithm.objects.get(pk=pk)
        assert al.has_access(request.user), "insufficient permissions"
        Algorithm.objects.get(pk=pk).delete()
        messages.success(request, 'Algorithm "%s" deleted' % al)
    except Exception, ex:
        messages.error(request, 'Algorithm not deleted: %s' % ex)
    finally:
        return redirect('algorithm:list')


# CLASS BASED VIEWS

class AlgorithmBaseView(object):
    model = Algorithm


class AlgorithmList(AlgorithmBaseView, ListView):
    template_name = "djspikeval/algorithm/list.html"


class AlgorithmCreate(AlgorithmBaseView, CreateView):
    template_name = "djspikeval/algorithm/create.html"
    form_class = AlgorithmForm

    def get_form_kwargs(self):
        kwargs = super(AlgorithmCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AlgorithmDetail(AlgorithmBaseView, DetailView):
    template_name = "djspikeval/algorithm/detail.html"


class AlgorithmUpdate(AlgorithmBaseView, UpdateView):
    template_name = "djspikeval/algorithm/update.html"
    form_class = AlgorithmForm

    def get_form_kwargs(self):
        kwargs = super(AlgorithmUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AlgorithmDelete(AlgorithmBaseView, DeleteView):
    template_name = "djspikeval/algorithm/delete.html"
    success_url = reverse_lazy("algorithm:list")


if __name__ == "__main__":
    pass
