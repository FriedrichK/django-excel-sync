from abc import ABCMeta, abstractmethod


class BaseSpreadsheetSource(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self._settings = kwargs

    def get(self, label):
        return self._settings[label]

    @abstractmethod
    def get_rows(field_settings):
        pass
