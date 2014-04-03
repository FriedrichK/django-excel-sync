from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from excel_sync.db.models.mixins import SpreadsheetModelMixin


@receiver(post_syncdb)
def import_spreadsheet_data(sender, **kwargs):
    if not sender.__name__ == 'excel_sync.models':
        return
    for klass in kwargs["created_models"]:
        if(is_spreadsheet_model(klass)):
            klass.import_spreadsheet_data(klass)


def is_spreadsheet_model(klass):
    if hasattr(klass._meta, 'spreadsheet_source'):
        return True
    return False
