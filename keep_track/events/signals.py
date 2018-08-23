from django.db.models.signals import ModelSignal


post_bulk_create = ModelSignal(
    providing_args=['ids', 'objs', 'batch_size'],
    use_caching=True,
)
post_mt_bulk_create = ModelSignal(
    providing_args=['ids', 'objs', 'batch_size'],
    use_caching=True,
)
post_update = ModelSignal(
    providing_args=['queryset', 'update_kwarg'],
    use_caching=True,
)
