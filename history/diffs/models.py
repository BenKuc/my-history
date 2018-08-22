from django.db.models import Model as DjangoModel
# TODO: J1,2,3,4


__all__ = [
    'Diff',
]


class Diff(DjangoModel):
    event = None  # TODO: unique with pk/id (OneToOne?)
