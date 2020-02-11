from django.db import models
from django.forms import CharField, Textarea


class StringListField(models.TextField):
    description = "Array of strings"

    def __init__(self, separator='\n', *args, **kwargs):
        self.separator = separator
        kwargs['max_length'] = None
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        return super().deconstruct()

    def db_type(self, connection):
        return 'stringlist'

    def get_internal_type(self):
        return "StringListField"

    def get_prep_value(self, value):
        return self.separator.join(value)

    def from_db_value(self, value, expression, connection):
        return value

    def to_python(self, value):
        if value is None:
            return None
        return [i for i in value.split(self.separator) if i]

    def value_to_string(self, obj):
        return self.separator.join(self.value_from_object(obj))

    def get_separator(self):
        return self.separator
