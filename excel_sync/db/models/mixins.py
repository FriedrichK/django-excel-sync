from excel_sync.db.models.fields import SpreadsheetMixin


class SpreadsheetModelMixin:
    @staticmethod
    def import_spreadsheet_data(klass):
        source = get_spreadsheet_datasource(klass)
        fields_with_spreadsheet_metadata = get_fields_with_spreadsheet_metadata(klass)
        field_settings = build_field_settings(fields_with_spreadsheet_metadata)
        data_for_rows = source.get_rows(field_settings)
        for data_for_row in data_for_rows:
            entry = klass(**data_for_row)
            entry.save()


def get_spreadsheet_datasource(klass):
    return klass._meta.spreadsheet_source


def get_fields_with_spreadsheet_metadata(klass):
    all_fields = klass._meta.fields
    fields_with_spreadsheet_metadata = []
    for field in all_fields:
        if(has_spreadsheet_metadata(field)):
            fields_with_spreadsheet_metadata.append(field)
    return fields_with_spreadsheet_metadata


def has_spreadsheet_metadata(field):
    return isinstance(field, SpreadsheetMixin)


def build_field_settings(fields_with_spreadsheet_metadata):
    field_settings = []
    for field in fields_with_spreadsheet_metadata:
        field_setting = field.get_spreadsheet_settings()
        field_settings.append(field_setting)
    return field_settings
