from django.db.models import Model as DjangoModel
# TODO: create a new app in which all this code lives! -> also to allow for custom migrations (data-migrations)

# TODO: diff classes -> same as model but with old and new on field and field/relation events

__all__ = [
    'Diff',
]


# TODO: this whole code must be thought through -> what is to be displayed by diffs on relations and so on?
class Diff(DjangoModel):
    event = None  # TODO: unique with pk/id (OneToOne?)
