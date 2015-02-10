##---IMPORTS

from django.contrib import admin
from .gnode_spike.apps.module.metric_ffranke.models import ResultMetricFFranke

##---ADMIN

class ResultMetricFFrankeAdmin(admin.ModelAdmin):
    pass

admin.site.register(ResultMetricFFranke, ResultMetricFFrankeAdmin)

##---MAIN

if __name__ == '__main__':
    pass
