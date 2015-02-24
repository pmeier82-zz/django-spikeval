# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url, include
from djspikeval import views

__author__ = "pmeier82"

patterns_algorithm = patterns(
    "",
    url(r"^$", views.AlgorithmList.as_view(), name="list"),
    url(r"^create/$", views.AlgorithmCreate.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", views.AlgorithmDetail.as_view(), name="detail"),
    url(r"^(?P<pk>\d+)/update/$", views.AlgorithmUpdate.as_view(), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", views.AlgorithmDelete.as_view(), name="delete"),
)

patterns_benchmark = patterns(
    "",
    url(r"^$", views.BenchmarkList.as_view(), name="list"),
    url(r"^create/$", views.BenchmarkCreate.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", views.BenchmarkDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/update/$', views.BenchmarkUpdate.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', views.BenchmarkDelete.as_view(), name="delete"),
    url(r"^(?P<pk>\d+)/toggle/$", views.BenchmarkToggle.as_view(), name="toggle"),
    url(r"^(?P<pk>\d+)/download/$", views.BenchmarkDownload.as_view(), name="download"),
)

patterns_evaluation = patterns(
    "",
    url(r"^$", views.SubmissionList.as_view(), name="list"),
    url(r"^list/(?P<pk>\d+)$", views.SubmissionList.as_view(), name="list-filter"),
    url(r"^create/(?P<pk>\d+)$", views.SubmissionCreate.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", views.SubmissionDetail.as_view(), name="detail"),
    url(r"^(?P<pk>\d+)/update/$", views.SubmissionUpdate.as_view(), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", views.SubmissionDelete.as_view(), name="delete"),
)

patterns_trial = patterns(
    "",
    url(r"create/(?P<pk>\d+)$", views.TrialCreate.as_view(), name="create"),
    url(r'^(?P<pk>\d+)/$', views.TrialDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/update/$', views.TrialUpdate.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', views.TrialDelete.as_view(), name="delete"),
    url(r'^(?P<pk>\d+)/validate/$', views.TrialValidate.as_view(), name="validate"),
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
