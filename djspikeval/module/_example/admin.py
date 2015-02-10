##---IMPORTS

from django.contrib import admin
from .gnode_spike.apps.module._example.models import ResultExample

##---ADMIN

class ResultExampleAdmin(admin.ModelAdmin):
    pass

admin.site.register(ResultExample, ResultExampleAdmin)

##---MAIN

if __name__ == '__main__':
    pass
