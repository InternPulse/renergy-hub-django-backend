from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allows clients to specify the page size in the query
    max_page_size = 100  # Maximum number of items per page allowed
    last_page_strings = ('last',)  # Optional: You can use 'last' as a query parameter for the last page
