import pydantic
from rest_framework.utils import encoders


class JSONEncoder(encoders.JSONEncoder):
    # for pydantic support
    def default(self, obj):
        if isinstance(obj, pydantic.BaseModel):
            return obj.dict()
        return super().default(obj)
