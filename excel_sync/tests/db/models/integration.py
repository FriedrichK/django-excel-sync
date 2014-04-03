from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
loading.cache.loaded = False

from mockito import *

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


def build_test_model_class():
    spreadsheet_source = mock()
    spreadsheet_source.get_rows = generate_rows

    fields = {
        'first_name': CharField(max_length=30, spreadsheet_column_number=1, spreadsheet_column_row=1),
        'last_name': CharField(max_length=30, spreadsheet_column_number=2, spreadsheet_column_row=2)
    }

    options = {
        'spreadsheet_source': spreadsheet_source
    }

    return generate_model(name='Person', module='excel_sync', fields=fields, options=options)
