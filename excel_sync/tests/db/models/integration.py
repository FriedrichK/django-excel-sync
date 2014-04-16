import os

from django.conf import settings
from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
loading.cache.loaded = False

from mockito import *

from excel_sync.contrib.spreadsheet.excel import ExcelSpreadsheetSource
from excel_sync.db.models.fields import CharField, IntegerField, FloatField

#from excel_sync.tests.models import Person
from excel_sync.tests._tools import generate_model, generate_rows


class MixinAndFieldsIntegrationTestCase(TestCase):

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
            'last_name': CharField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=2),
            'age': IntegerField(max_length=30, spreadsheet_column_number=5, spreadsheet_column_row=2),
            'correct': FloatField(spreadsheet_column_number=7, spreadsheet_column_row=2)
        }
        Employees = build_model("employees", spreadsheet_source, fields)
        call_command('syncdb', verbosity=0, interactive=False)

        actual = Employees.objects.all().values()

        expected = [{u'first_name': u'John', u'last_name': u'Doe', u'id': 1, u'age': 21, u'correct': 0.5}, {u'first_name': u'Jane', u'last_name': u'D.', u'id': 2, u'age': 32, u'correct': 0.933}]
        self.assertEqual(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])

    def test_model_with_real_data_saves_expected_rows_with_absolute_and_relative_columns(self):
        spreadsheet_source = ExcelSpreadsheetSource(data_source=os.path.join(settings.TEST_DATA, 'testworksheet02.xls'), worksheet_name='Sheet1', row_start=3)
        fields = {
            'correct': FloatField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=2),
            'questions': IntegerField(max_length=30, spreadsheet_column_number=1, spreadsheet_column_row=2),
            'correct_pcnt': FloatField(max_length=30, spreadsheet_column_number=3, spreadsheet_column_row=3, spreadsheet_percentage=True, spreadsheet_reference_column_number=1),
            'correct_abs': IntegerField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=3, spreadsheet_absolute=True, spreadsheet_reference_column_number=1),
        }
        Employees = build_model("employees2", spreadsheet_source, fields)
        call_command('syncdb', verbosity=0, interactive=False)

        actual = Employees.objects.all().values()

        expected = [{u'id': 1, u'questions': 30, u'correct': 0.5, u'correct_pcnt': 0.5, u'correct_abs': 15}, {u'id': 2, u'questions': 30, u'correct': 0.933, u'correct_pcnt': 0.93, u'correct_abs': 28}]
        self.assertEqual(expected[0], actual[0])
        self.assertEqual(expected[1], actual[1])

    def test_model_with_real_data_saves_expected_rows_with_absolute_and_relative_columns_where_reference_is_zero(self):
        spreadsheet_source = ExcelSpreadsheetSource(data_source=os.path.join(settings.TEST_DATA, 'testworksheet03.xls'), worksheet_name='Sheet1', row_start=3)
        fields = {
            'correct': FloatField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=2),
            'questions': IntegerField(max_length=30, spreadsheet_column_number=1, spreadsheet_column_row=2),
            'correct_pcnt': FloatField(max_length=30, spreadsheet_column_number=3, spreadsheet_column_row=3, spreadsheet_percentage=True, spreadsheet_reference_column_number=1),
            'correct_abs': IntegerField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=3, spreadsheet_absolute=True, spreadsheet_reference_column_number=1),
        }
        Employees = build_model("employees3", spreadsheet_source, fields)
        call_command('syncdb', verbosity=0, interactive=False)

        actual = Employees.objects.all().values()

        expected = [{u'id': 1, u'questions': 0, u'correct': 0.5, u'correct_pcnt': 0.0, u'correct_abs': 0}, {u'id': 2, u'questions': 0, u'correct': 0.933, u'correct_pcnt': 0.0, u'correct_abs': 0}]
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
