import xlrd

from excel_sync.spreadsheet import BaseSpreadsheetSource


class ExcelSpreadsheetSource(BaseSpreadsheetSource):

    def get_rows(self, field_settings):
        columns = self._get_columns_from_field_settings(field_settings)
        row_start = self.get('row_start')
        filtered_rows = self._get_filtered_rows(field_settings, columns, row_start)
        database_rows = self._generate_database_rows(field_settings, filtered_rows)
        database_rows = self._process_options(field_settings, database_rows)
        return database_rows

    def _get_columns_from_field_settings(self, field_settings):
        columns = []
        for field_setting in field_settings:
            columns.append(field_setting['column'] - 1)
        return columns

    def _get_filtered_rows(self, field_settings, columns, row_start):
        worksheet = self._get_worksheet()
        rows = self._get_rows_from_worksheet(worksheet, columns, row_start)
        return rows

    def _get_worksheet(self):
        workbook = self._open_xlrd_source(self.get('data_source'))
        return workbook.sheet_by_name(self.get('worksheet_name'))

    def _open_xlrd_source(self, path):
        return xlrd.open_workbook(path)

    def _get_rows_from_worksheet(self, worksheet, columns, row_start):
        rows = []

        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1

        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            if not self._start_of_data_rows_reached(curr_row, row_start):
                continue
            rows.append(self._get_cells_from_row(worksheet, num_cells, curr_row, columns))
        return rows

    def _start_of_data_rows_reached(self, curr_row, row_start):
        return (curr_row >= row_start - 1)

    def _get_cells_from_row(self, worksheet, num_cells, curr_row, columns):
        row = []
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            if not curr_cell in columns:
                continue
            row.append(self._get_cell_info_from_cell(worksheet, curr_row, curr_cell))
        return row

    def _get_cell_info_from_cell(self, worksheet, curr_row, curr_cell):
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        #cell_type = worksheet.cell_type(curr_row, curr_cell)
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        return cell_value

    def _generate_database_rows(self, field_settings, filtered_rows):
        field_settings_sorted_by_column = self._sort_field_settings_by_column(field_settings)

        database_rows = []
        for row in filtered_rows:
            database_row = self._build_database_row(field_settings_sorted_by_column, row)
            database_rows.append(database_row)
        return database_rows

    def _sort_field_settings_by_column(self, field_settings):
        return sorted(field_settings, key=lambda setting: setting['column'])

    def _build_database_row(self, field_settings, row):
        database_row = {}
        for i in range(len(field_settings)):
            database_row[field_settings[i]['name']] = row[i]
        return database_row

    def _get_values_for_column(self, column, starting_row):
        column = column - 1
        worksheet = self._get_worksheet()
        values = []

        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1

        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            if not self._start_of_data_rows_reached(curr_row, starting_row):
                continue
            cell = self._get_cells_from_row(worksheet, num_cells, curr_row, [column])[0]
            values.append(cell)
        return values
