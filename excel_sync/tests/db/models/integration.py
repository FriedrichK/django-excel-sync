import os

from django.conf import settings
from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
loading.cache.loaded = False

from mockito import *

from excel_sync.contrib.spreadsheet.excel import ExcelSpreadsheetSource
from excel_sync.db.models.fields import CharField

#from excel_sync.tests.models import Person
from excel_sync.tests._tools import generate_model, generate_rows


class MixinAndCharFieldIntegrationTestCase(TestCase):

    def test_model_saves_expected_rows(self):
        Person = build_test_model_class()
        call_command('syncdb', verbosity=0, interactive=False)
        entries = Person.objects.all().values()

        self.assertEqual(10, len(entries))
        self.assertEqual({'first_name': u'entry0', 'last_name': u'entry0', u'id': 1}, entries[0])

    def test_model_with_real_data_saves_expected_rows(self):
        spreadsheet_source = ExcelSpreadsheetSource(data_source=os.path.join(settings.TEST_DATA, 'testworksheet01.xls'), worksheet_name='Sheet1', row_start=3)
        fields = {
            'first_name': CharField(max_length=30, spreadsheet_column_number=1, spreadsheet_column_row=1),
            'last_name': CharField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=2)
        }
        Employees = build_model("employees", spreadsheet_source, fields)
        call_command('syncdb', verbosity=0, interactive=False)

        actual = Employees.objects.all().values()

        expected = [{'first_name': u'John', 'last_name': u'Doe', u'id': 1}, {'first_name': u'Jane', 'last_name': u'D.', u'id': 2}]
        self.assertEqual(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])


def build_test_model_class():
    name = "Person"
    spreadsheet_source = build_spreadsheet_source()
    fields = build_fields()
    return build_model(name, spreadsheet_source, fields)


def build_spreadsheet_source():
    spreadsheet_source = mock()
    spreadsheet_source.get_rows = generate_rows
    return spreadsheet_source


def build_fields():
    return {
        'first_name': CharField(max_length=30, spreadsheet_column_number=1, spreadsheet_column_row=1),
        'last_name': CharField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=2)
    }


def build_model(name, spreadsheet_source, fields):
    options = {
        'spreadsheet_source': spreadsheet_source
    }

    return generate_model(name=name, module='excel_sync', fields=fields, options=options)