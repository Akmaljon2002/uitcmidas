from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import Serializer, IntegerField, CharField, ListField


class CustomOffSetPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


def paginate(instances, serializator, request, **kwargs):
    paginator = CustomOffSetPagination()
    paginated_order = paginator.paginate_queryset(instances, request)

    serializer = serializator(paginated_order, many=True, **kwargs)

    return paginator.get_paginated_response(serializer.data)


class PaginationGetSerializer(Serializer):
    count = IntegerField()
    next = CharField(allow_blank=True, allow_null=True)
    previous = CharField(allow_blank=True, allow_null=True)
    results = ListField()

    def __init__(self, *args, **kwargs):
        result_serializer = kwargs.pop('result_serializer', None)
        super().__init__(*args, **kwargs)

        if result_serializer is not None:
            self.fields['results'] = ListField(child=result_serializer())