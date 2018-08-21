from collections import namedtuple

DEFAULT_ITERABLES = (list, tuple, set, )
EXTRA_FIELDS_SIGNATURE = {'instance', ''}

# TODO: more information by model-cls and so on
# TODO: make a class out of it that sets variable automatically?
# TODO: better replace by django-checks

HISTORY_ERROR_MESSAGES = {
    'DEFAULT_ITERABLES': "Attribute {name} must an instance of one of the "
                         "following iterables: {iterables}.",
    'TUPLE_REQUIRED': "Element must be of type tuple.",
    'LENGTH_THREE': "tuple requires length three: name, field, value.",
    'NAME_STRING': "name needs to be a string.",
    'FIELD_DJANGO': "field needs to be an instance of django.db.models.Field",
    'WRONG_SIGNATURE': "Function requires to have attributes: "
                       "instance and request.",
    'EXTRA_FIELDS_ERROR': "Following errors were detected on attribute {}: {}",
}
