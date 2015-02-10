##---IMPORTS

from django.contrib import admin
from .gnode_spike.apps.module.default_visual.models import ResultDefaultVisual

##---ADMIN

class ResultDefaultVisualAdmin(admin.ModelAdmin):
    pass

admin.site.register(ResultDefaultVisual, ResultDefaultVisualAdmin)

##---MAIN

if __name__ == '__main__':
    pass
