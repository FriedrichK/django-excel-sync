from django.test import TestCase

from mock import Mock

from excel_sync.contrib.spreadsheet.excel import ExcelSpreadsheetSource


class ExcelTestCase(TestCase):

    def test_does_something(self):

        xlrd_mock = Mock()
        xlrd_mock.configure_mock(**{
            'sheet_by_name.return_value.nrows': 2,
            'sheet_by_name.return_value.ncols': 4,
            'sheet_by_name.return_value.cell_type.return_value': 1,
            'sheet_by_name.return_value.cell_value.return_value': 2
        })

        data_source = ExcelSpreadsheetSource(data_source='path/to/not_an_actual_file.xlsx', worksheet_name='not_a_real_worksheet', row_start=2)
        data_source._open_xlrd_source = Mock()
        data_source._open_xlrd_source.return_value = xlrd_mock

        field_settings_mock = [
            {'name': 'first_name', 'column': 0, 'label_row': 1},
            {'name': 'last_name', 'column': 1, 'label_row': 0}
        ]

        actual = data_source.get_rows(field_settings_mock)

        expected = [{'first_name': 2, 'last_name': 2}]
        self.assertEqual(expected, actual)
