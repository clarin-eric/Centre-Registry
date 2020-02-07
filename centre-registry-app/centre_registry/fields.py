from django.db import models


class StringListField(models.TextField):
    description = "Array of strings"

    def __init__(self, separator=';', *args, **kwargs):
        self.separator = separator
        kwargs['max_length'] = None
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.separator != ';':
            kwargs['separator'] = self.separator
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.separator.join(value)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return value.split(self.separator)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
