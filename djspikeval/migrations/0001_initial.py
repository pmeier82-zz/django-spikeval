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
        ('base', '0002_auto_20150223_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(default=b'0.1', max_length=32)),
                ('description', models.TextField(blank=True)),
                ('kind', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name=b'Kind')),
                ('owner', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='djspikeval.Algorithm', null=True)),
            ],
            options={
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
                ('status', model_utils.fields.StatusField(default=b'private', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'private', b'private'), (b'public', b'public')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('name', models.CharField(help_text=b'The name will be used as an identifier for the Benchmark. (character limit: 255)', max_length=255, verbose_name='name')),
                ('description', models.TextField(help_text=b'Use this field to give a detailed description of the Benchmark. Although there is no limit to the content of this field, you may want to provide an attached file if your space or editing requirements are not met. (character limit: none)', blank=True)),
                ('parameter', models.CharField(default=b'No.', help_text=b'Individual Trials of the Benchmark can have a parameter attached that can be used to order and distinguish the Trials. This may be a simulation or experimental parameter that has been varied systematically or just a numbering (default). (character limit: 255)', max_length=255)),
                ('owner', models.ForeignKey(related_name='benchmarks', default=2, to=settings.AUTH_USER_MODEL, help_text=b'The user who contributed this Benchmark.')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=b'A comma-separated list of tags classifying the Benchmark.', verbose_name='Benchmark Tags')),
            ],
            options={
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
                ('status', model_utils.fields.StatusField(default=b'initial', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'initial', b'initial'), (b'running', b'running'), (b'success', b'success'), (b'failure', b'failure')])),
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
                ('status', model_utils.fields.StatusField(default=b'private', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'private', b'private'), (b'public', b'public')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('description', models.TextField(null=True, blank=True)),
                ('algorithm', models.ForeignKey(default=1, to='djspikeval.Algorithm', help_text=b'The Algorithm associated with this submission.')),
                ('benchmark', models.ForeignKey(related_name='submission_set', to='djspikeval.Benchmark', help_text=b'The Benchmark associated with this submission.')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'The user associated with this submission.')),
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
                ('name', models.CharField(help_text=b'The name will be used as an identifier for the Trial. (character limit: 255)', max_length=255)),
                ('description', models.TextField(help_text=b'Use this field to give a detailed description of the Benchmark. Although there is no limit to the content of this field, you may want to provide an attached file if your space or editing requirements are not met. (character limit: none)', blank=True)),
                ('parameter', models.FloatField(default=0.0, help_text=b'The parameter value for this Trial. (type: float)')),
                ('valid_rd_log', models.TextField(null=True, blank=True)),
                ('valid_gt_log', models.TextField(null=True, blank=True)),
                ('gt_type', models.CharField(default=b'total', help_text=b'Type of ground truth for this Trial.\nTotal: all events are explained;\nPartial: some events are explained, there may or may not be additional events not detailed in the ground truth;\nNone: no ground truth is provided;', max_length=20, choices=[(b'total', b'total'), (b'partial', b'partial'), (b'none', b'none')])),
                ('gt_access', models.CharField(default=b'private', help_text=b'Access mode for the ground truth files if provided.', max_length=20, choices=[(b'private', b'private'), (b'public', b'public')])),
                ('benchmark', models.ForeignKey(help_text=b'The Benchmark associated with this Trial.', to='djspikeval.Benchmark')),
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
        migrations.CreateModel(
            name='Attachment',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('base.asset',),
        ),
        migrations.CreateModel(
            name='Datafile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('base.asset',),
        ),
    ]
