from django.db.models.fields import CharField as VanillaCharField, IntegerField as VanillaIntegerField, FloatField as VanillaFloatField
from django.db import models
from django.core.exceptions import FieldError


class SpreadsheetMixin(object):

    required_field_options = ['spreadsheet_column_number', 'spreadsheet_column_row']
    optional_field_options = ['spreadsheet_percentage', 'spreadsheet_absolute', 'spreadsheet_reference_column_number']

    def __init__(self, *args, **kwargs):
        self._validate_custom_field_options(**kwargs)
        self._spreadsheet_column_number = kwargs['spreadsheet_column_number']
        self._spreadsheet_column_row = kwargs['spreadsheet_column_row']
        self._spreadsheet_options = {}
        for option in self.optional_field_options:
            if option in kwargs:
                self._spreadsheet_options[option] = kwargs[option]
        kwargs = self._remove_custom_field_options(**kwargs)
        super(SpreadsheetMixin, self).__init__(*args, **kwargs)

    def get_spreadsheet_column_number(self):
        return self._spreadsheet_column_number

    def get_spreadsheet_column_row(self):
        return self._spreadsheet_column_row

    def get_spreadsheet_options(self):
        return self._spreadsheet_options

    def get_spreadsheet_settings(self):
        return {
            'name': self.name,
            'column': self.get_spreadsheet_column_number(),
            'label_row': self.get_spreadsheet_column_row(),
            'options': self.get_spreadsheet_options()
        }

    def _validate_custom_field_options(self, **kwargs):
        for required_field_option in self.required_field_options:
            if not required_field_option in kwargs:
                raise FieldError('field option %s is required' % required_field_option)
        return True

    def _remove_custom_field_options(self, **kwargs):
        for required_field_option in self.required_field_options:
            del kwargs[required_field_option]
        for option in self._spreadsheet_options:
            del kwargs[option]
        return kwargs


class CharField(SpreadsheetMixin, VanillaCharField):
    description = "A CharField using data from a spreadsheet"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)


class IntegerField(SpreadsheetMixin, VanillaIntegerField):
    description = "An IntegerField using data from a spreadsheet"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)


class FloatField(SpreadsheetMixin, VanillaFloatField):
    description = "A FloatField using data from a spreadsheet"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)
