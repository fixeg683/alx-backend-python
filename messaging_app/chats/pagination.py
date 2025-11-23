# chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class MessagesPagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    - Default page size: 20
    - Page query param: ?page=<number>
    - Max page size: 100
    """
    page_size = 20
    page_query_param = "page"
    max_page_size = 100


# Backwards-compatible alias: some settings or imports expect `MessagePagination` (singular).
# Provide an alias so `from chats.pagination import MessagePagination` works.
MessagePagination = MessagesPagination
