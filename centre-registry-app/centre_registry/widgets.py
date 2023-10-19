from django.forms import TextInput


class ArrayFieldInputWidget(TextInput):
    """
    Custom widget for rendering postgres array fields in forms

    Input is ABC inheriting Widget ABC
    """

    input_type = None
    separator: str = ','
    template_name = "widgets/_arrayfield_widget.html"

    def __int__(self, separator=',', **kwargs):
        super().__init__(**kwargs)
        self.separator = separator

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a template.
        """
        if isinstance(value, list):
            return value
        return value.split(self.separator)
