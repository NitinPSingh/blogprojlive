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
                    
                    )
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('', BlogListView.as_view(), name='home'),
    path('post/new',BlogCreateView.as_view(),name='post_new'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),

    path('register/',register,name='register'),
    path('like/<int:pk>',LikeView,name='like_post'),
    path('post/<int:pk>/comment',CommentCreateView.as_view(),name='comment_post'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
