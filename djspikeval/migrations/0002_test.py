# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from django.db import models, migrations


def test_data(apps, schema_editor):
    # admin user
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    admin_user = User.objects.get(pk=1)

    # test algo
    Algorithm = apps.get_model("djspikeval", "algorithm")
    obj_al = Algorithm()
    obj_al.name = "Test Algorithm"
    obj_al.version = "0.1"
    obj_al.description = "Initial Algorithm for testing purposes."
    obj_al.user = admin_user
    obj_al.save()

    # test dataset
    Dataset = apps.get_model("djspikeval", "dataset")
    obj_ds = Dataset()
    obj_ds.name = "Test Dataset"
    obj_ds.description = "Initial Dataset for testing purposes."
    obj_ds.parameter = "No."
    obj_ds.user = User.objects.get(pk=1)
    obj_ds.save()


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
        ("initial_data", "0001_initial"),
        ("djspikeval", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(test_data),
    ]

