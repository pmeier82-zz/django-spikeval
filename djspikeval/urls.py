# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from djspikeval import views

__author__ = "pmeier82"

## ALGORITHM

patterns_algorithm = patterns(
    "djspikeval.views.algorithm",
    url(r'^$', views.AlgorithmList.as_view(), name="list"),
    url(r'^create/$', views.AlgorithmCreate.as_view(), name="create"),
    url(r'^(?P<pk>\d+)/$', views.AlgorithmDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/update/$', views.AlgorithmUpdate.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', views.AlgorithmDelete.as_view(), name="delete"),
)

patterns_benchmark = patterns(
    "djspikeval.views.benchmark",
    url(r"^$", views.BenchmarkList.as_view(), name="list"),
    url(r"^create/$", views.BenchmarkCreate.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", views.BenchmarkDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/update/$', views.BenchmarkUpdate.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', views.BenchmarkDelete.as_view(), name="delete"),
    url(r"^(?P<pk>\d+)/toggle/$", views.BenchmarkToggle.as_view(), name="toggle"),
    url(r"^(?P<pk>\d+)/summary/$", views.BenchmarkSummary.as_view(), name="summary"),
    # url(r"^(?P<bm_pk>\d+)/summary_plot/(?P<mod_pk>\d+)/(?P<mode>\w+)/$", "summary_plot",
    # {"legend": False}, name="summary_plot"),
    url(r"^(?P<pk>\d+)/download/$", views.BenchmarkDownload.as_view(), name="download"),
    url(r"^(?P<pk>\d+)/trial/$", views.TrialCreate.as_view(), name="trial"),
)

patterns_evaluation = patterns(
    "djspikeval.views.evaluation",
    url(r"^$", "list", name="list"),
    url(r"^(?P<pk>\d+)/$", "list", name="list"),  # list constrained for benchmark
    url(r"^detail/(?P<pk>\d+)/$", "detail", name="detail"),
    url(r"^delete/(?P<pk>\d+)/$", "delete", name="delete"),
    url(r"^toggle/(?P<pk>\d+)/$", "toggle", name="toggle"),
    url(r"^zip/(?P<pk>\d+)/$", "zip", name="zip"),
    url(r"^run/(?P<pk>\d+)/$", "run", name="run"),
)

patterns_trial = patterns(
    "djspikeval.views.trial",
    url(r'^(?P<pk>\d+)/$', views.TrialDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/update/$', views.TrialUpdate.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', views.TrialDelete.as_view(), name="delete"),
)

urlpatterns = patterns(
    "",
    url(r"^algorithm/", include(patterns_algorithm, namespace="algorithm")),
    url(r"^benchmark/", include(patterns_benchmark, namespace="benchmark")),
    url(r"^evaluation/", include(patterns_evaluation, namespace="evaluation")),
    url(r"^trial/", include(patterns_trial, namespace="trial")),
)
if __name__ == "__main__":
    pass
