from django.db import models
from django.forms import CharField, Textarea
from django.utils.encoding import smart_str


class StringListField(models.CharField):
    description = "Array of strings"

    def __init__(self, separator=';', *args, **kwargs):
        self.separator = separator
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        return super().deconstruct()

    def db_type(self, connection):
        return 'stringlist'

    def get_internal_type(self):
        return "StringListField"

    def get_prep_value(self, value):
        if value is None:
            return ''
        else:
            return self.separator.join(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return []
        return value.split(self.separator)

    def get_db_prep_save(self, value, connection):
        if value is None:
            return ''
        return self.separator.join(value)

    def value_to_string(self, obj):
        return self.separator.join(self.value_from_object(obj))
