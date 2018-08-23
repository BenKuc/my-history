import inspect

from django.db.models.fields import Field as DjangoField

from keep_track.common.constants import (
    DEFAULT_ITERABLES, HISTORY_ERROR_MESSAGES, EXTRA_FIELDS_SIGNATURE,
)


def assert_iterable(name, obj):
    base_msg = HISTORY_ERROR_MESSAGES['DEFAULT_ITERABLES']
    msg = base_msg.format(name, DEFAULT_ITERABLES)
    assert isinstance(obj, DEFAULT_ITERABLES), msg


def assert_correct_three_tuple(name, field, value):
    errors = []
    if not isinstance(name, str):
        errors.append(HISTORY_ERROR_MESSAGES['NAME_STRING'])
    if not isinstance(field, DjangoField):
        errors.append(HISTORY_ERROR_MESSAGES['FIELD_DJANGO'])

    if callable(value):
        sig = inspect.signature(value)
        if not set(sig.parameters.keys()) == EXTRA_FIELDS_SIGNATURE:
            errors.append(HISTORY_ERROR_MESSAGES['WRONG_SIGNATURE'])
    return errors


def assert_three_tuple_iterable(name, obj):
    assert_iterable(name, obj)

    errors = []
    for idx, element in enumerate(obj):
        idx_errors = []
        if not isinstance(element, tuple):
            idx_errors.append(HISTORY_ERROR_MESSAGES['TUPLE_REQUIRED'])
        elif len(element) == 3:
            idx_errors.append(HISTORY_ERROR_MESSAGES['LENGTH_THREE'])
        else:
            idx_errors.append(assert_correct_three_tuple(element))
        if idx_errors:
            errors.append(
                "Error on index {}: {}".format(idx, ' '.join(idx_errors))
            )

    assert not errors, HISTORY_ERROR_MESSAGES['EXTRA_FIELDS_ERROR'].format(
        name, ' & '.join(errors))
