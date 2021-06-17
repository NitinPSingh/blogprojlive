from django.urls import path
from .views import (
                    BlogListView,
                    BlogUpdateView,
                    BlogDetailView,
                    BlogCreateView,
                    BlogDeleteView,
                    register,
                    LikeView,
                    CommentCreateView,
                    DetailPost,
                    ListPost,
                    search,
                    user_login
                    )
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('', BlogListView.as_view(), name='home'),
    path('post/new',BlogCreateView.as_view(),name='post_new'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
    path('apidetail/<int:pk>/', DetailPost.as_view()),
    path('apilist', ListPost.as_view()),
    path('search',search,name='search'),
    path('register/',register,name='register'),
    path('like/<int:pk>',LikeView,name='like_post'),
    path('post/<int:pk>/comment',CommentCreateView.as_view(),name='comment_post'),
    path('login/',user_login, name='login'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
