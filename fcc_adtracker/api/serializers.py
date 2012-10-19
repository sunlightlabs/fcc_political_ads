import unicodecsv
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from tastypie.serializers import Serializer


class ExpandedSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'csv']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'csv': 'text/csv',
    }

    def to_csv(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        object_list = data.get('objects', [])
        for obj in object_list:
            for k, v in obj.items():
                if isinstance(v, list):
                   obj[k] = ','.join(v)
        if len(object_list):
            raw_data = StringIO()
            dict_fields = object_list[0].keys()
            dict_fields.sort()
            writer = unicodecsv.DictWriter(raw_data, dict_fields, extrasaction='ignore')
            writer.writeheader()
            for item in object_list:
                writer.writerow(item)
            raw_data.seek(0)
            output = raw_data.read()
            return output
        else:
            return ''

