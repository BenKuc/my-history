from django.db import models


__all__ = [
    'ObjectEvent',
]


# TODO: consistency: same (content)type + same id -> CHECK-constraint
# TODO: create indexes in history_date and ...
# TODO: next and previous
# TODO: event and next_event -> this probably goes on the model
# TODO: check constraints for before and after
# TODO: do check constraints that prevent saving before/after when the type
#       is create/update -> sql
class ObjectEvent(models.Model):
    """
    An instance of this always belongs to a ManagerEvent-instance.
    """
    trigger = models.CharField(
        # TODO: add all operations in Atomic-history?
        choices=(
            ('QB', 'queryset: bulk_create'),
            ('QU', 'queryset: update'),
            ('QD', 'queryset: delete'),
            ('D', 'delete'),
            ('CS', 'creation by save'),
            ('US', 'update by save')
        )
    )
    # TODO: check-constraint that this corresponds to trigger (actually this
    #       does not need db-column? -> but filtering?)
    # TODO: also check constraints for before and after concerning this
    type = models.CharField(
        choices=(
            ('C', 'creation'),
            ('U', 'update'),
            ('D', 'deletion'),
        )
    )
    # TODO: this must be adjusted to differences-boolean
    #       -> field is added if True, otherwise not
    # TODO: if true -> consistency checks
    diff = None
    object_history = models.ForeignKey(
        'history.ObjectHistory', related_name='events', on_delete=models.CASCADE,
    )
    history_date = models.DateTimeField(auto_now_add=True)

    before = models.OneToOneField(
        'history.HistoryBaseModel',
        null=True,
        on_delete=models.CASCADE,
        related_name='next_event',
    )
    after = models.OneToOneField(
        'history.HistoryBaseModel',
        null=True,
        on_delete=models.CASCADE,
        related_name='previous_event',
    )

    class Meta:
        # TODO: order_by history_date!
        order_by = ()

    def __str__(self):
        return '{type}-event triggered by '

    # TODO: do we really need this here?
    @property
    def history_id(self):
        return self.object_history.model

    # TODO: do we really need this here?
    @property
    def id(self):
        return self.object_history.model

    # TODO: do we really need this here?
    @property
    def model(self):
        return self.object_history.co
