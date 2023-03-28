from django.db import models


class StringArrayField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(StringArrayField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        ret = None
        if isinstance(value, list):
            ret = value
        elif value:
            ret = value.split(self.token)
        return ret

    # arguments to match parent method signature
    def get_db_prep_value(self, value, connection, prepared: bool = False):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_db_prep_value(value)