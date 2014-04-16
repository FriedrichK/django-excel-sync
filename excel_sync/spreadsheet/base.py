from abc import ABCMeta, abstractmethod

from django.core.exceptions import FieldError


class BaseSpreadsheetSource(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rows(field_settings):
        pass

    def __init__(self, **kwargs):
        self._settings = kwargs

    def get(self, label):
        return self._settings[label]

    def get_rows(self, field_settings):
        pass

    def _process_options(self, field_settings, database_rows):
        for field_setting in field_settings:
            database_rows = self._process_options_for_field(field_setting, database_rows)
        return database_rows

    def _process_options_for_field(self, field_setting, database_rows):
        if not 'options' in field_setting:
            return database_rows

        if 'spreadsheet_percentage' in field_setting['options']:
            if not 'spreadsheet_reference_column_number' in field_setting['options']:
                raise FieldError('field %s is set to mode spreadsheet_percentage but lacks required option spreadsheet_reference_column_number' % field_setting['name'])
            database_rows = self._process_option_percentage(field_setting, database_rows)

        if 'spreadsheet_absolute' in field_setting['options']:
            if not 'spreadsheet_reference_column_number' in field_setting['options']:
                raise FieldError('field %s is set to mode spreadsheet_absolute but lacks required option spreadsheet_reference_column_number' % field_setting['name'])
            database_rows = self._process_option_absolute(field_setting, database_rows)

        return database_rows

    def _process_option_percentage(self, field_setting, database_rows):
        reference_column_number = field_setting['options']['spreadsheet_reference_column_number']
        values_start_at = field_setting['label_row']
        values_for_reference_column = self._get_values_for_column(reference_column_number, values_start_at)
        value_field_name = field_setting['name']
        for i in range(len(database_rows)):
            if not self._is_a_number(database_rows[i][value_field_name]) or not self._is_a_number(values_for_reference_column[i]):
                continue
            pcnt = database_rows[i][value_field_name] / values_for_reference_column[i]
            database_rows[i][value_field_name] = int(pcnt * 100.0) / 100.0
        return database_rows

    def _process_option_absolute(self, field_setting, database_rows):
        reference_column_number = field_setting['options']['spreadsheet_reference_column_number']
        values_start_at = field_setting['label_row']
        values_for_reference_column = self._get_values_for_column(reference_column_number, values_start_at)
        value_field_name = field_setting['name']
        for i in range(len(database_rows)):
            if not self._is_a_number(database_rows[i][value_field_name]) or not self._is_a_number(values_for_reference_column[i]):
                continue
            absolute = int(round(database_rows[i][value_field_name] * values_for_reference_column[i]))
            database_rows[i][value_field_name] = absolute
        return database_rows

    def _is_a_number(self, candidate):
        try:
            float(candidate)
            return True
        except ValueError:
            return False
