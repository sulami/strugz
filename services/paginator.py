from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(items, num, page):
    """Paginate a list of items"""

    paginator = Paginator(items, num)
    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated

