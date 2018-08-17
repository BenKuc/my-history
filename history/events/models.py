from django.db.models import Model as DjangoModel
# TODO: create a new app in which all this code lives! -> also to allow for custom migrations (data-migrations)


class Event(DjangoModel):
    event_id = None
    event_date = None
    user = None
    # TODO: this must be adjusted to differences-boolean -> field is added if True, otherwise not
    # TODO: if true -> consistency checks
    diff = None
    trigger_method = None # TODO: choices: bulk_create, delete, update, save

    # TODO: referenced pks of objects must be the same + unique with the event_id

    # TODO: next and previous
    # TODO: event and next_event -> this probably goes on the model


class Update(Event):
    # TODO: FK to history instance -> Generic-FK
    # TODO: consistency: same (content)type + same id -> CHECK-constraint
    # TODO: next and previous for Event and event and next_event
    before = None
    after = None


class Creation(Event):
    after = None


class Deletion(Event):
    before = None
