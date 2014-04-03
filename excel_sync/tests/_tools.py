from django.db import models
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('spreadsheet_source',)

from excel_sync.db.models import SpreadsheetModelMixin


def generate_model(name=None, module=None, fields=None, options=None):
    class Meta:
        pass

    app_label = 'excel_sync'
    if app_label:
        setattr(Meta, 'app_label', app_label)

    if options:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    attrs = {'__module__': module, 'Meta': Meta}

    if fields:
        attrs.update(fields)

    return type(name, (models.Model, SpreadsheetModelMixin), attrs)


def generate_rows(field_data):
    fake_data = []
    items = 10
    for i in range(items):
        item = {}
        for field in field_data:
            item[field['name']] = "entry%s" % i
        fake_data.append(item)
    return fake_data
