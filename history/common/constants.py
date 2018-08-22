DEFAULT_ITERABLES = (list, tuple, set, )
EXTRA_FIELDS_SIGNATURE = {'instance', 'request'}


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
