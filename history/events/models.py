from django.db import models

from ..diffs.models import Diff


__all__ = [
    'ObjectEvent',
]


# TODO: I
class ObjectEvent(models.Model):
    """
    An instance of this always belongs to a ManagerEvent-instance.
    """
    type = models.CharField(
        choices=(
            ('C', 'creation'),
            ('U', 'update'),
            ('D', 'deletion'),
        )
    )
    diff = models.OneToOneField(Diff, on_delete=models.CASCADE, null=True)
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
        order_by = ['+history_data']

    def __str__(self):
        return '{}-event at {}.'.format(self.type, self.history_date)
