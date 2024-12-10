import re
from collections import OrderedDict

from pydantic import BaseModel
from rest_framework import renderers
from django.utils.encoding import force_str
from django.utils.functional import Promise
from djangorestframework_camel_case import util as dcc_util
from djangorestframework_camel_case import render
from djangorestframework_camel_case.settings import api_settings
from rest_framework.utils.serializer_helpers import ReturnDict

from utils.encoders import JSONEncoder


class JSONRenderer(renderers.JSONRenderer):
    encoder_class = JSONEncoder


# Forked `djangorestframework_camel_case.camelize` due to lack of support for pydantic models.
def camelize(data, **options):  # noqa: C901
    # Handle lazy translated strings.
    ignore_fields = options.get("ignore_fields") or ()
    if isinstance(data, Promise):
        data = force_str(data)

    if isinstance(data, BaseModel):
        data = data.dict()

    if isinstance(data, dict):
        if isinstance(data, ReturnDict):
            new_dict = ReturnDict(serializer=data.serializer)
        else:
            new_dict = OrderedDict()
        for key, value in data.items():
            if isinstance(key, Promise):
                key = force_str(key)
            if isinstance(key, str) and "_" in key:
                new_key = re.sub(dcc_util.camelize_re, dcc_util.underscore_to_camel, key)
            else:
                new_key = key
            if key not in ignore_fields and new_key not in ignore_fields:
                new_dict[new_key] = camelize(value, **options)
            else:
                new_dict[new_key] = value
        return new_dict
    if dcc_util.is_iterable(data) and not isinstance(data, str):
        return [camelize(item, **options) for item in data]
    return data


class CamelCaseJSONRenderer(render.CamelCaseJSONRenderer):
    def render(self, data, *args, **kwargs):
        return super().render(
            camelize(data, **self.json_underscoreize),
            *args,
            **kwargs,
        )


class CamelCaseBrowsableAPIRenderer(render.BrowsableAPIRenderer):
    def render(self, data, *args, **kwargs):
        return super().render(camelize(data, **api_settings.JSON_UNDERSCOREIZE), *args, **kwargs)
