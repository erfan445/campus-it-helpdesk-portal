from django.core.paginator import Paginator


def paginate_queryset(request, queryset, per_page=12):
    """Small helper used by list views to keep pagination consistent."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def empty_to_none(value):
    value = value.strip() if isinstance(value, str) else value
    return value or None
