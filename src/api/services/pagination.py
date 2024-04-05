from enum import Enum
from ninja import Schema

from api.schemas import PaginationResponseBody

import inspect
from functools import partial, wraps
from typing import Any, Callable, Tuple, Type

from asgiref.sync import sync_to_async
from django.db.models import QuerySet, Q
from ninja.constants import NOT_SET
from ninja.pagination import LimitOffsetPagination, PaginationBase, make_response_paginated
from ninja.types import DictStrAny


class AsyncLimitOffsetPagination(LimitOffsetPagination):
    async def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: LimitOffsetPagination.Input,
        **params: DictStrAny,
    ):
        offset = pagination.offset
        limit: int = pagination.limit

        @sync_to_async
        def process_query_set():
            return {
                "items": queryset[offset : offset + limit] if queryset else [],
                "count": self._items_count(queryset) if queryset else 0,
            }

        return await process_query_set()


def apaginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: DictStrAny) -> Callable:

    isfunction = inspect.isfunction(func_or_pgn_class)
    isnotset = func_or_pgn_class == NOT_SET

    pagination_class: Type[PaginationBase] = AsyncLimitOffsetPagination

    if isfunction:
        return _inject_pagination(func_or_pgn_class, pagination_class)

    if not isnotset:
        pagination_class = func_or_pgn_class

    def wrapper(func: Callable) -> Any:
        return _inject_pagination(func, pagination_class, **paginator_params)

    return wrapper


def _inject_pagination(
    func: Callable,
    paginator_class: Type[PaginationBase],
    **paginator_params: Any,
) -> Callable:
    paginator: PaginationBase = paginator_class(**paginator_params)

    @wraps(func)
    async def view_with_pagination(*args: Tuple[Any], **kwargs: DictStrAny) -> Any:
        pagination_params = kwargs.pop("ninja_pagination")
        if paginator.pass_parameter:
            kwargs[paginator.pass_parameter] = pagination_params

        items = await func(*args, **kwargs)

        result = await paginator.paginate_queryset(items, pagination=pagination_params, **kwargs)
        if paginator.Output:
            result[paginator.items_attribute] = list(result[paginator.items_attribute])
            # ^ forcing queryset evaluation #TODO: check why pydantic did not do it here
        return result

    view_with_pagination._ninja_contribute_args = [  # type: ignore
        (
            "ninja_pagination",
            paginator.Input,
            paginator.InputSource,
        ),
    ]

    if paginator.Output:
        view_with_pagination._ninja_contribute_to_operation = [partial(  # type: ignore
            make_response_paginated,
            paginator,
        ),]

    return view_with_pagination

class SortDirs(Enum):
    asc = "asc"
    desc = "desc"


class PaginationWithOrdering(LimitOffsetPagination):
    class Input(Schema):
        sortBy: str = "createdAt"
        sortDir: SortDirs = SortDirs.asc
        limit: int = 10
        page: int = 1
        search: str

    class Output(PaginationResponseBody):
        pass

    items_attribute = "data"

    async def paginate_queryset(self, queryset: QuerySet, pagination: Input, **params):
        sort_by = ('-' if pagination.sortDir == SortDirs.desc else '') + pagination.sortBy
        print(sort_by)
        queryset = queryset.order_by(sort_by)
        search_str = pagination.search
        # searching
        queryset = queryset.filter(
            Q(name__contains=search_str) |
            Q(surname__contains=search_str) |
            Q(patronymic__contains=search_str) |
            Q(typeEducation__contains=search_str) |
            Q(livingAddress__city__contains=search_str) |
            Q(livingAddress__city__contains=search_str)
        )

        limit = pagination.limit
        page = pagination.page

        @sync_to_async
        def process_query_set():
            return {"limit": limit, "page": page, "total": self._items_count(queryset) if queryset else 0,
                    "data": queryset[(page-1) * limit: (page-1) * limit + limit]}

        return await process_query_set()
