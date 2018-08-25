from django.db.models import QuerySet, Subquery, OuterRef, Max


# TODO: refactor this after
# TODO: set a settings option to use this manager/queryset
# TODO: inspect query behaviour!
# TODO: distinguish between arbitrary multi and the query for existing object!
class MultiplePKRobustQuerySet(QuerySet):

    def for_multiplicity_easy(self, multi, pk):
        """
        Args:
            multi: The multiplicity of how often the pk-value was regiven
            pk: The pk-value

        Returns: Filter the given queryset for all track-entries that match
                 the given pk and multiplicity.
        """
        # TODO: this must be all(), not self
        model = None
        some_date = None
        creation_date = model.objects.order_by('+track_date').filter(
            type='C', track_date__lte=some_date,
        ).last().track_date
        # TODO: this is not correct! -> here you need another query...
        latest_date = model.objects.order_by('+track_date').filter(
            type='D', track_date__lte=some_date,
        ).first().track_date
        return model.objets.filter(
            track_date__gte=creation_date, track_date__lte=latest_date,
        )

    def for_multiplicity(self, multi, pk):
        model = None
        some_date = None
        model.objects.annotate(
            creation_date=Subquery(
                model.objects.filter(
                    type='C', track_date__lte=OuterRef('track_date'),
                ).aggregate(max=Max('track_date'))['max']
            ),
            # TODO: this is also not correct -> for existing object this
            #       cannot be evaluated (see also above)
            latest_date=Subquery(
                model.objects.filter(
                    type='D', track_date__lte=OuterRef('track_date'),
                ).aggregate(max=Max('track_date'))['max'],
            ),
        ).filter(
            creation_date__lte=some_date,
            latest_date__gte=some_date,
        )
