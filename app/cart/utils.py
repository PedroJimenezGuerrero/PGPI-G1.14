import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super(DecimalEncoder, self).default(obj)

