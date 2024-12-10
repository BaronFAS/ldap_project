from rest_framework.pagination import PageNumberPagination

from cloud_core.settings import LARGE_PAGINATION_PAGE_SIZE


class LargeResultsSetPagination(PageNumberPagination):
    page_size = LARGE_PAGINATION_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = LARGE_PAGINATION_PAGE_SIZE
