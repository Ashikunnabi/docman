from collections import OrderedDict

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class LargeResultsSetPagination(LimitOffsetPagination):
    limit_query_param = "length"
    offset_query_param = "start"
    max_limit = 100
    kwargs = {}

    def set_paginated_kwargs(self, **kwargs):
        self.kwargs = kwargs

    def get_paginated_response(self, data):
        try:
            draw = self.request.query_params.get("draw")
        except MultiValueDictKeyError:
            draw = 1

        return Response(
            OrderedDict(
                [
                    ("recordsTotal", self.count),
                    ("recordsFiltered", self.count),
                    ("draw", draw),
                    ("data", data),
                    ("kwargs", self.kwargs),
                ]
            )
        )


class CustomLargeResultsSetPagination(LimitOffsetPagination):
    limit_query_param = "length"
    offset_query_param = "start"
    max_limit = 100000000

    def get_paginated_response(self, data):
        try:
            draw = self.request.query_params.get("draw")
        except MultiValueDictKeyError:
            draw = 1

        return Response(
            OrderedDict(
                [
                    ("recordsTotal", self.count),
                    ("recordsFiltered", self.count),
                    ("draw", draw),
                    ("data", data),
                ]
            )
        )


class CustomResultsSetPageWisePagination(PageNumberPagination):
    page_query_param = "page"
    page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
