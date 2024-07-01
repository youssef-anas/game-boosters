from django.urls import path
from news.views import  CreateBlogView, BlogHomeView, BlogDetailsView

urlpatterns = [
    path('', BlogHomeView.as_view(), name='blog_home'),
    path('create/', CreateBlogView.as_view(), name='blog_create'),
    path('<int:id>/',BlogDetailsView.as_view(), name="blog_details_view" ),
    # path('order/', CreateBlogOrderView.as_view(), name='blog_order_create'),
]