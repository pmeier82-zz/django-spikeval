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
                ('owner', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='djspikeval.Algorithm', null=True)),
            ],
            options={
                'ordering': ('-modified', 'name', 'version'),
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Benchmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='private', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('private', 'private'), ('public', 'public')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('name', models.CharField(help_text='The name will be used as an identifier for the Benchmark. (character limit: 255)', max_length=255, verbose_name='name')),
                ('description', models.TextField(help_text='Use this field to give a detailed description of the Benchmark. Although there is no limit to the content of this field, you may want to provide an attached file if your space or editing requirements are not met. (character limit: none)', blank=True)),
                ('parameter', models.CharField(default='No.', help_text='Individual Trials of the Benchmark can have a parameter attached that can be used to order and distinguish the Trials. This may be a simulation or experimental parameter that has been varied systematically or just a numbering (default). (character limit: 255)', max_length=255)),
                ('kind', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags classifying the Benchmark.', verbose_name='Benchmark Kind')),
                ('owner', models.ForeignKey(related_name='benchmarks', default=2, to=settings.AUTH_USER_MODEL, help_text='The user who contributed this Benchmark.')),
            ],
            options={
                'ordering': ('-modified', 'name'),
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='initial', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('initial', 'initial'), ('running', 'running'), ('success', 'success'), ('failure', 'failure')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('task_id', models.CharField(max_length=255, null=True, blank=True)),
                ('task_log', models.TextField(null=True, blank=True)),
                ('valid_ev_log', models.TextField(null=True, blank=True)),
            ],
            options={
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
                ('benchmark', models.ForeignKey(related_name='submission_set', to='djspikeval.Benchmark', help_text='The Benchmark associated with this submission.')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='The user associated with this submission.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(help_text='The name will be used as an identifier for the Trial. (character limit: 255)', max_length=255)),
                ('description', models.TextField(help_text='Use this field to give a detailed description of the Benchmark. Although there is no limit to the content of this field, you may want to provide an attached file if your space or editing requirements are not met. (character limit: none)', blank=True)),
                ('parameter', models.FloatField(default=0.0, help_text='The parameter value for this Trial. (type: float)')),
                ('valid_rd_log', models.TextField(null=True, blank=True)),
                ('valid_gt_log', models.TextField(null=True, blank=True)),
                ('gt_type', models.CharField(default='total', help_text='Type of ground truth for this Trial.\nTotal: all events are explained;\nPartial: some events are explained, there may or may not be additional events not detailed in the ground truth;\nNone: no ground truth is provided;', max_length=20, choices=[('total', 'total'), ('partial', 'partial'), ('none', 'none')])),
                ('gt_access', models.CharField(default='private', help_text='Access mode for the ground truth files if provided.', max_length=20, choices=[('private', 'private'), ('public', 'public')])),
                ('benchmark', models.ForeignKey(help_text='The Benchmark associated with this Trial.', to='djspikeval.Benchmark')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='trial',
            unique_together=set([('benchmark', 'parameter')]),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='submission',
            field=models.ForeignKey(to='djspikeval.Submission'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='trial',
            field=models.ForeignKey(to='djspikeval.Trial'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='algorithm',
            unique_together=set([('name', 'version')]),
        ),
    ]
