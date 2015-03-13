# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import apps
from django.contrib import admin

__author__ = "pmeier82"

Algorithm = apps.get_registered_model("djspikeval", "algorithm")
Analysis = apps.get_registered_model("djspikeval", "analysis")
Datafile = apps.get_registered_model("djspikeval", "datafile")
Dataset = apps.get_registered_model("djspikeval", "dataset")
Module = apps.get_registered_model("djspikeval", "module")
Result = apps.get_registered_model("djspikeval", "result")
Submission = apps.get_registered_model("djspikeval", "submission")


class AlgorithmAdmin(admin.ModelAdmin):
    pass


class AnalysisAdmin(admin.ModelAdmin):
    pass


class DatafileAdmin(admin.ModelAdmin):
    pass


class DatasetAdmin(admin.ModelAdmin):
    pass


class ModuleAdmin(admin.ModelAdmin):
    pass


class ResultAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(Datafile, DatafileAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Submission, SubmissionAdmin)

if __name__ == "__main__":
    pass
