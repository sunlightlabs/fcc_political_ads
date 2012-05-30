from django import forms

try:
    import simplejson as json
except Exception, e:
    import json


class TypeaheadTextInput(forms.TextInput):
    attrs = {
        'class':'typeahead',
        'autocomplete': 'off',
        'data-provide': 'typeahead',
        'maxlength': 100
    }

    def __init__(self, data_source=None, attrs=None):
        if not attrs:
            attrs = self.attrs.copy()
        if data_source:
            if not isinstance(data_source, list):
                raise TypeError('data_source must be a list')
            attrs['data-source'] = json.dumps(data_source)
        super(TypeaheadTextInput, self).__init__(attrs)

