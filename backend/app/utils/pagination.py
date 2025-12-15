from flask import request


def get_pagination_args(default_size: int = 10):
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", default_size))
    except ValueError:
        page, size = 1, default_size
    page = max(1, page)
    size = max(1, min(size, 100))
    return page, size


def paginate_query(query, page: int, size: int):
    pagination = query.paginate(page=page, per_page=size, error_out=False)
    return {
        "items": [item.to_dict() for item in pagination.items],
        "page": pagination.page,
        "size": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    }
