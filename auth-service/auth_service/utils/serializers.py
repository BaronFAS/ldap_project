from rest_framework.serializers import ModelSerializer


class RestrictUpdateMixin:
    """Adds support to allow only certain fields to be updated.

    To use it, specify a list of fields as `updatable_fields` on the
    serializer's Meta:
    ```
    class Meta:
        model = SomeModel
        fields = '__all__'
        updatable_fields = ('collection', )
    ```

    Now the fields in `updatable_fields` can be set during POST (create),
    but can be changed afterwards via PUT or PATCH (update).
    Inspired by http://stackoverflow.com/a/37487134/627411.
    """

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()

        # We're only interested in PATCH/PUT.
        if "update" in getattr(self.context.get("view"), "action", ""):
            return self._set_write_once_fields(extra_kwargs)

        return extra_kwargs

    def _set_write_once_fields(self, extra_kwargs):
        """Set all fields in `Meta.write_once_fields` to read_only."""
        updatable_fields = getattr(self.Meta, "updatable_fields", None)
        if not updatable_fields:
            return extra_kwargs

        if not isinstance(updatable_fields, (list, tuple)):
            raise TypeError(
                "The `updatable_fields` option must be a list or tuple. "
                "Got {}.".format(type(updatable_fields).__name__)
            )

        for field_name in getattr(self.Meta, "fields", None):
            if field_name not in updatable_fields:
                kwargs = extra_kwargs.get(field_name, {})
                kwargs["read_only"] = True
                extra_kwargs[field_name] = kwargs

        return extra_kwargs


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DynamicFieldsQueryMixin:
    def get_serializer(self, *args, **kwargs):
        """
        In addition to choosing a serializer, the *fields* parameter is also checked and, if present,
        passed to the serializer to reduce the output of fields.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        query_fields = kwargs["context"]["request"].query_params.get("fields")
        if query_fields:
            fields = [f.strip() for f in query_fields.split(",")]
            kwargs["fields"] = fields

        return serializer_class(*args, **kwargs)
