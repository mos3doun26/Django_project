from django.urls import path
from . import views
from .views import PostListview, PostDetailview, PostCreateview, PostUpdateview, PostDeleteview, UserPostListview

urlpatterns = [
    path("", PostListview.as_view(), name="blog-home"),
    path("user/<str:username>", UserPostListview.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailview.as_view(), name="post-detail"),
    path("post/new/", PostCreateview.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateview.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteview.as_view(), name="post-delete"),
    path("about/", views.about, name="blog-about")
]
