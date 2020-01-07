from django.urls import path
from .views import *

urlpatterns = [
    path('', all_blogs),
    path('add/', add_blog),

    path('api/blog/', api_blog_list),
    path('api/blog/(?P[0-9]+)', api_blog_detail),
]