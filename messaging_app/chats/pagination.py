from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    # 20 messages per page
    page_size = 20
    page_size_query_param = 'page_size'  # Optional: allow clients to override
    max_page_size = 100

    # Optional: customize the paginated response
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)
