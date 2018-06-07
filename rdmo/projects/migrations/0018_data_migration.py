# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-28 11:23
from __future__ import unicode_literals

from django.db import migrations


def set_value_unit_and_type(apps, schema_editor):
    Value = apps.get_model('projects', 'Value')

    for value in Value.objects.all():
        try:
            value.value_type = value.attribute.value_type
        except AttributeError:
            value.value_type = 'text'

        try:
            value.unit = value.attribute.unit or ''
        except AttributeError:
            value.unit = ''

        value.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_value_unit_and_type'),
    ]

    operations = [
        migrations.RunPython(set_value_unit_and_type),
    ]
