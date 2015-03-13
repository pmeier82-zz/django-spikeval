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

patterns_dataset = patterns(
    "",
    url(r"^$", views.DatasetList.as_view(), name="list"),
    url(r"^create/$", views.DatasetCreate.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", views.DatasetDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/update/$', views.DatasetUpdate.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', views.DatasetDelete.as_view(), name="delete"),
    url(r"^(?P<pk>\d+)/toggle/$", views.DatasetToggle.as_view(), name="toggle"),
    url(r"^(?P<pk>\d+)/download/$", views.DatasetDownload.as_view(), name="download"),
)

patterns_analysis = patterns(
    "",
    url(r"^$", views.AnalysisList.as_view(), name="list"),
    url(r"^list/(?P<pk>\d+)$", views.AnalysisList.as_view(), name="list-filter"),
    url(r"^create/(?P<pk>\d+)$", views.AnalysisCreate.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", views.AnalysisDetail.as_view(), name="detail"),
    url(r"^(?P<pk>\d+)/update/$", views.AnalysisUpdate.as_view(), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", views.AnalysisDelete.as_view(), name="delete"),
    url(r"^(?P<pk>\d+)/toggle/$", views.AnalysisToggle.as_view(), name="toggle"),
    url(r"^(?P<pk>\d+)/download/$", views.AnalysisDownload.as_view(), name="download"),
    url(r"^(?P<pk>\d+)/start/$", views.AnalysisStart.as_view(), name="start"),
    url(r"^(?P<pk>\d+)/start-all/$", views.AnalysisSubmissionStart.as_view(), name="start-all"),
)

patterns_datafile = patterns(
    "",
    url(r"create/(?P<pk>\d+)$", views.DatafileCreate.as_view(), name="create"),
    url(r'^(?P<pk>\d+)/$', views.DatafileDetail.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/update/$', views.DatafileUpdate.as_view(), name="update"),
    url(r'^(?P<pk>\d+)/delete/$', views.DatafileDelete.as_view(), name="delete"),
    url(r'^(?P<pk>\d+)/validate/$', views.DatafileValidate.as_view(), name="validate"),
)

urlpatterns = patterns(
    "",
    url(r"^algorithm/", include(patterns_algorithm, namespace="algorithm")),
    url(r"^analysis/", include(patterns_analysis, namespace="analysis")),
    url(r"^datafile/", include(patterns_datafile, namespace="datafile")),
    url(r"^dataset/", include(patterns_dataset, namespace="dataset")),
)

if __name__ == "__main__":
    pass
