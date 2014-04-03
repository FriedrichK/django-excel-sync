import os

from django.test import TestCase
from django.conf import settings

from mock import Mock

from excel_sync.contrib.spreadsheet.excel import ExcelSpreadsheetSource

PATH_TO_TEST_WORKBOOK = os.path.join(settings.TEST_DATA, 'testworksheet01.xls')


class ExcelTestCase(TestCase):

    def test_returns_expected_data_from_mocked_workbook(self):

        xlrd_mock = Mock()
        xlrd_mock.configure_mock(**{
            'sheet_by_name.return_value.nrows': 2,
            'sheet_by_name.return_value.ncols': 4,
            'sheet_by_name.return_value.cell_type.return_value': 1,
            'sheet_by_name.return_value.cell_value.return_value': 2
        })

        data_source = ExcelSpreadsheetSource(data_source='path/to/not_an_actual_file.xlsx', worksheet_name='not_a_real_worksheet', row_start=1)
        data_source._open_xlrd_source = Mock()
        data_source._open_xlrd_source.return_value = xlrd_mock

        field_settings_mock = [
            {'name': 'first_name', 'column': 1, 'label_row': 1},
            {'name': 'last_name', 'column': 2, 'label_row': 0}
        ]

        actual = data_source.get_rows(field_settings_mock)

        self.assertEqual(2, len(actual))

    def test_returns_expected_data_from_actual_workbook(self):
        field_settings_mock = [
            {'name': 'first_name', 'column': 1, 'label_row': 1},
            {'name': 'last_name', 'column': 2, 'label_row': 0}
        ]

        data_source = ExcelSpreadsheetSource(data_source=PATH_TO_TEST_WORKBOOK, worksheet_name='Sheet1', row_start=3)

        actual = data_source.get_rows(field_settings_mock)

        expected = [{'first_name': u'John', 'last_name': u'Doe'}, {'first_name': u'Jane', 'last_name': u'D.'}]
        self.assertEqual(expected, actual)
