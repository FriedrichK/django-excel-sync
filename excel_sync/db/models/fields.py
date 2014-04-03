from django.db.models.fields import CharField as VanillaCharField
from django.db import models
from django.core.exceptions import FieldError


class SpreadsheetMixin(object):

    required_field_options = ['spreadsheet_column_number', 'spreadsheet_column_row']

    def __init__(self, *args, **kwargs):
        self._validate_custom_field_options(**kwargs)
        self._spreadsheet_column_number = kwargs['spreadsheet_column_number']
        self._spreadsheet_column_row = kwargs['spreadsheet_column_row']
        kwargs = self._remove_custom_field_options(**kwargs)
        super(SpreadsheetMixin, self).__init__(*args, **kwargs)

    def get_spreadsheet_column_number(self):
        return self._spreadsheet_column_number

    def get_spreadsheet_column_row(self):
        return self._spreadsheet_column_row

    def get_spreadsheet_settings(self):
        return {
            'name': self.name,
            'column_number': self.get_spreadsheet_column_number(),
            'column_row': self.get_spreadsheet_column_row()
        }

    def _validate_custom_field_options(self, **kwargs):
        for required_field_option in self.required_field_options:
            if not required_field_option in kwargs:
                raise FieldError('field option %s is required' % required_field_option)
        return True

    def _remove_custom_field_options(self, **kwargs):
        for required_field_option in self.required_field_options:
            del kwargs[required_field_option]
        return kwargs


class CharField(SpreadsheetMixin, VanillaCharField):
    description = "A CharField using data from a spreadsheet"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
