# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(default='0.1', max_length=32)),
                ('description', models.TextField(blank=True)),
                ('kind', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags classifying the Algorithm.', verbose_name='Algorithm Kind')),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='djspikeval.Algorithm', null=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', 'name', 'version'),
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='initial', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('initial', 'initial'), ('running', 'running'), ('success', 'success'), ('failure', 'failure')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('task_id', models.CharField(max_length=255, null=True, blank=True)),
                ('task_log', models.TextField(null=True, blank=True)),
                ('valid_st_log', models.TextField(null=True, blank=True)),
            ],
            options={
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Datafile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(help_text='The name will be used as an identifier for the Datafile. (character limit: 255)', max_length=255)),
                ('description', models.TextField(help_text='Use this field to give a detailed description of the Dataset. Although there is no limit to the content of this field, you may want to provide an attached file if your space or editing requirements are not met. (character limit: none)', blank=True)),
                ('parameter', models.FloatField(default=0.0, help_text='The parameter value for this Datafile. (type: float)')),
                ('valid_rd_log', models.TextField(null=True, blank=True)),
                ('valid_gt_log', models.TextField(null=True, blank=True)),
                ('gt_type', models.CharField(default='total', help_text='Type of ground truth for this Datafile.\nTotal: all events are explained;\nPartial: some events are explained, there may or may not be additional events not detailed in the ground truth;\nNone: no ground truth is provided;', max_length=20, choices=[('total', 'total'), ('partial', 'partial'), ('none', 'none')])),
                ('gt_access', models.CharField(default='private', help_text='Access mode for the ground truth files if provided.', max_length=20, choices=[('private', 'private'), ('public', 'public')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='private', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('private', 'private'), ('public', 'public')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('name', models.CharField(help_text='The name will be used as an identifier for the Dataset. (character limit: 255)', max_length=255, verbose_name='name')),
                ('description', models.TextField(help_text='Use this field to give a detailed description of the Dataset. Although there is no limit to the content of this field, you may want to provide an attached file if your space or editing requirements are not met. (character limit: none)', blank=True)),
                ('parameter', models.CharField(default='No.', help_text='Individual Trials of the Dataset can have a parameter attached that can be used to order and distinguish the Trials. This may be a simulation or experimental parameter that has been varied systematically or just a numbering (default). (character limit: 255)', max_length=255)),
                ('kind', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags classifying the Dataset.', verbose_name='Dataset Kind')),
                ('user', models.ForeignKey(related_name='benchmarks', default=2, to=settings.AUTH_USER_MODEL, help_text='The user who contributed this Dataset.')),
            ],
            options={
                'ordering': ('-modified', 'name'),
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='private', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('private', 'private'), ('public', 'public')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('description', models.TextField(null=True, blank=True)),
                ('algorithm', models.ForeignKey(default=1, to='djspikeval.Algorithm', help_text='The Algorithm associated with this submission.')),
                ('dataset', models.ForeignKey(related_name='submission_set', to='djspikeval.Dataset', help_text='The Dataset associated with this submission.')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='The user associated with this submission.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='datafile',
            name='dataset',
            field=models.ForeignKey(help_text='The Dataset associated with this Datafile.', to='djspikeval.Dataset'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='datafile',
            unique_together=set([('dataset', 'parameter')]),
        ),
        migrations.AddField(
            model_name='analysis',
            name='datafile',
            field=models.ForeignKey(to='djspikeval.Datafile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analysis',
            name='submission',
            field=models.ForeignKey(to='djspikeval.Submission'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='algorithm',
            unique_together=set([('name', 'version')]),
        ),
    ]
