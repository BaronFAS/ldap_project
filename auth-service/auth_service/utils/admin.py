from django.contrib import admin


def custom_titled_filter(title, filter_class):
    """A custom wrapper for list filter that allows to change filter title"""

    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = filter_class.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper
