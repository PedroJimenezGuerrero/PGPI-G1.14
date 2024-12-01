from django.core.signing import JSONSerializer as BaseJSONSerializer
from .utils import DecimalEncoder
import json

class JSONSerializer(BaseJSONSerializer):
    def dumps(self, obj):
        return json.dumps(obj, separators=(',', ':'), cls=DecimalEncoder).encode('latin-1')