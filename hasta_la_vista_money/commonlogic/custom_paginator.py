from django.core.paginator import Page, Paginator


def paginator_custom_view(request, queryset, paginate_by, page_name) -> Page:
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
