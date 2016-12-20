# -*- coding: utf-8 -*-
import abc
import click


class BaseDataImporter(object):

    def __new__(cls):
        for field in cls.field_relation.keys():
            def _method(self, data):
                return data
            if not hasattr(cls, 'clean_' + field):
                setattr(cls, 'clean_' + field, _method)
        return super(BaseDataImporter, cls).__new__(cls)

    @abc.abstractmethod
    def get_data(self):
        return

    @abc.abstractmethod
    def get_model(self):
        return

    def get_progressbar_label(self):
        return 'Importing data'

    def after_save_object(self, obj):
        pass

    def save_data(self):
        print('Downloading data...')
        data = self.get_data()
        if isinstance(data, dict):
            self._get_object(data)
        elif isinstance(data, list):
            with click.progressbar(data,
                                   label=self.get_progressbar_label()) as data:
                for data_row in data:
                    self._get_object(data_row)

    def _get_object(self, data):
        obj = self._fill_model(self.get_model(), data)
        self.after_save_object(obj)
        return obj

    def _fill_model(self, model_class, data):
        obj_dict = {}

        for field in self.field_relation.keys():
            try:
                clean_method = getattr(self, 'clean_' + field)
                key = self.field_relation[field]
                cleaned_field = clean_method(data.get(key, None))

                if cleaned_field == '':
                    cleaned_field = None

                obj_dict[field] = cleaned_field
            except KeyError:
                continue
        obj, created = model_class.objects.get_or_create(**obj_dict)
        return obj
