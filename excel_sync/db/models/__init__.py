from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from excel_sync.db.models.mixins import SpreadsheetModelMixin

models_processed = []


@receiver(post_syncdb)
def import_spreadsheet_data(sender, **kwargs):
    models_left_to_process = get_models_left_to_process(kwargs["created_models"])
    for klass in models_left_to_process:
        if(is_spreadsheet_model(klass)):
            klass.import_spreadsheet_data(klass)


def is_spreadsheet_model(klass):
    if hasattr(klass._meta, 'spreadsheet_source'):
        return True
    return False


def get_models_left_to_process(models):
    global models_processed
    models_left_to_process = []
    for model in models:
        if not model in models_processed:
            models_left_to_process.append(model)
    models_processed += models_left_to_process
    return models_left_to_process
