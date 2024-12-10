import typing
import logging
from functools import partial

import pydantic
from django.db.models import JSONField
from django.db.migrations.writer import MigrationWriter
from django.core.serializers.json import DjangoJSONEncoder
from django.db.migrations.serializer import BaseSerializer


logger = logging.getLogger(__name__)
PDModelType = typing.Type[pydantic.BaseModel]


def default_error_handler(obj, errors):
    logger.warning(
        "Can not parse stored object with schema obj=%s, errors=%s",
        obj,
        errors,
    )
    return obj


def try_parse(schema, obj):
    if isinstance(obj, str):
        return schema.parse_raw(obj)
    return schema.parse_obj(obj)


class FieldToPythonSetter:
    """
    Forces Django to call to_python on fields when setting them.
    This is useful when you want to add some custom field data postprocessing.
    Should be added to field like a so:
    ```
    def contribute_to_class(self, cls, name, *args, **kwargs):
        super().contribute_to_class(cls, name,  *args, **kwargs)
        setattr(cls, name, FieldToPythonSetter(self))
    ```
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, cls=None):
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class JSONSchemedEncoder(DjangoJSONEncoder):
    def __init__(self, *args, schema: typing.Union[typing.Tuple[PDModelType], PDModelType], **kwargs):
        if not isinstance(schema, tuple):
            self.schemas = (schema,)
        else:
            self.schemas = schema
        super().__init__(*args, **kwargs)

    def encode(self, obj):
        if not isinstance(obj, pydantic.BaseModel):
            # this flow used for expressions like .filter(data__contains={})
            # we don't want that {} to be parsed as schema
            return super().encode(obj)
        return obj.json()


class JSONSchemedDecoder:
    def __init__(
        self,
        schema: typing.Union[typing.Tuple[PDModelType], PDModelType],
        error_handler=default_error_handler,
    ):
        if not isinstance(schema, tuple):
            self.schemas = (schema,)
        else:
            self.schemas = schema
        self.error_handler = error_handler

    def decode(self, obj):
        if isinstance(obj, self.schemas):
            return obj

        errors = []
        for schema in self.schemas:
            try:
                return try_parse(schema, obj)
            except pydantic.ValidationError as exc:
                errors.append((schema, exc.errors()))
            except TypeError as exc:
                errors.append((schema, str(exc)))

        return self.error_handler(obj, errors)


class JSONSchemedField(JSONField):
    def __init__(self, *args, schema=None, error_handler=default_error_handler, **kwargs):
        kwargs.pop("encoder", None)
        kwargs.pop("decoder", None)
        super().__init__(*args, **kwargs)

        self._schemas = self._populate_schemas(schema)
        self.decoder = JSONSchemedDecoder(schema=self._schemas, error_handler=error_handler)
        self.encoder = partial(JSONSchemedEncoder, schema=self._schemas)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["schema"] = self._schemas
        kwargs.pop("encoder", None)
        kwargs.pop("decoder", None)
        return name, path, args, kwargs

    @staticmethod
    def _populate_schemas(schema) -> typing.Tuple[PDModelType]:  # noqa: C901
        if schema is None:
            raise ValueError("Schema can not be None")

        if isinstance(schema, tuple):
            return schema

        if isinstance(schema, type) and issubclass(schema, pydantic.BaseModel):
            return (schema,)

        origin = getattr(schema, "__origin__", None)
        if origin is typing.Union:
            for s in schema.__args__:
                if not issubclass(s, pydantic.BaseModel):
                    raise ValueError("Schema must be is subclass of `pydantic.BaseModel`")

            return schema.__args__

        # only pydantic.BaseModel and typing.Union are supported
        raise ValueError("Unsupported schema type: {0}".format(type(schema)))

    def to_python(self, value):
        if value is None:
            return None

        return self.decoder.decode(value)

    def from_db_value(self, value, expression, connection):
        return self.decoder.decode(value)

    def contribute_to_class(self, cls, name, *args, **kwargs):
        super().contribute_to_class(cls, name, *args, **kwargs)
        setattr(cls, name, FieldToPythonSetter(self))


class JSONSchemedDecoderSerializer(BaseSerializer):
    def serialize(self):
        return "utils.fields.JSONSchemedDecoder", set()


MigrationWriter.register_serializer(JSONSchemedDecoder, JSONSchemedDecoderSerializer)
