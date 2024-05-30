from django.urls import path
from news.views import  CreateBlogView, BlogHomeView

urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog_home'),
    path('create/', CreateBlogView.as_view(), name='blog_create'),
    # path('order/', CreateBlogOrderView.as_view(), name='blog_order_create'),
]