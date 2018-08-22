from django.db import models


# TODO: complete this
__all__ = [
    'ObjectEvent', 'Update', 'Creation', 'Deletion',
]


# TODO: this must be adjusted to differences-boolean
#       -> field is added if True, otherwise not
# TODO: if true -> consistency checks
class Event(models.Model):
    event_id = None
    event_date = None
    user = None

    diff = None
    trigger_method = None # TODO: choices: bulk_create, delete, update, save

    # TODO: referenced pks of objects must be the same + unique with the event_id

    # TODO: next and previous
    # TODO: event and next_event -> this probably goes on the model


class HistoryEvent(models.Model):
    pass


class ManagerEvent(models.Model):
    # TODO: type + reference to object_event?
    pass


# TODO: consistency: same (content)type + same id -> CHECK-constraint
# TODO: create indexes in history_date and
class ObjectEvent(models.Model):
    super_event = models.OneToOneField(ManagerEvent)
    # TODO: related_query_name?
    object_history = models.ForeignKey('history.ObjectHistory', related_name='events')
    history_date = ''
    type = ['UPDATE', 'CREATE', 'BULK_CREATE', 'BULK_UPDATE', ]
    # TODO: maybe wrap all create/update methods on queryset
    #       to get accurate all types
    trigger = ['save', 'bulk_create', 'bulk_update']  # TODO: move to ManagerEvent

    def __str__(self):
        return '{type}-event triggered by '

    # TODO: order_by history_date!


# TODO: also we need a direct reference to the history_id and so on...
# TODO: check constraints for before and after
# TODO: maybe remove this in favor of ObjectEvent -> type is a computed value by before and after -> get control over setattr by type
# TODO: do check constraints that prevent saving before/after when the type is create/update -> sql
class Creation(ObjectEvent):
    # TODO: this should actually have o2o field to object_history with related_name creation
    after = models.ForeignKey('history.PseudoHistoryModel', related_name='previous_event')


class Update(ObjectEvent):
    # TODO: FK to history instance -> Generic-FK
    # TODO: next and previous for Event and event and next_event
    before = models.ForeignKey('history.PseudoHistoryModel', related_name='next_event')
    after = models.ForeignKey('history.PseudoHistoryModel', related_name='previous_event')


class Deletion(ObjectEvent):
    # TODO: this should actually have o2o field to object_history with related_name deletion
    before = models.ForeignKey('history.Pseudo...', related_name='next_event')

    # TODO: also o2o field to tracking_connetion to another instance -> maybe in
    #       the future
