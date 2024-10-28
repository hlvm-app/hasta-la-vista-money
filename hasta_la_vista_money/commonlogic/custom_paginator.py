from typing import Any, Sequence, TypeVar

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

T = TypeVar('T')


def paginator_custom_view(
    request,
    queryset: QuerySet[Any],
    paginate_by: int,
    page_name: str,
) -> Page[Sequence[T]]:
    """
    Кастомный пагинатор для данных.

    :param request
    :param queryset
    :param paginate_by
    :param page_name
    :return Page

    """
    paginator = Paginator(queryset, paginate_by)
    num_page = request.GET.get(page_name)
    return paginator.get_page(num_page)
