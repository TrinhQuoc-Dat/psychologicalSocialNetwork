from rest_framework.pagination import PageNumberPagination

class CommentPaginator(PageNumberPagination):
    page_size = 5 
    page_query_param = 'page'
    max_page_size = 100


class PostPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 100


    
class SurveyPostPaginator(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 100


class ContactPaginator(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 100


class NotificationPaginator(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 100

