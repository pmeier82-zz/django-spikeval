# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from djspikeval.models import Module


class CheckModulesCommand(BaseCommand):
    args = "<poll_id poll_id ...>"
    help = "Do something with Module the specified poll for voting"
    requires_model_validation = True

    def handle(self, *args, **options):
        for pk in args:
            try:
                obj = Module.objects.get(pk=pk)
            except Module.DoesNotExist:
                raise CommandError("Module \"{}\" does not exist.".format(pk))

            obj.save()

            self.stdout.write("Successfully closed poll \"\"".format(pk))


if __name__ == "__main__":
    pass
