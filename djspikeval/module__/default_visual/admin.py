# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from .models import ResultDefaultVisual


class ResultDefaultVisualAdmin(admin.ModelAdmin):
    pass


admin.site.register(ResultDefaultVisual, ResultDefaultVisualAdmin)

if __name__ == "__main__":
    pass
