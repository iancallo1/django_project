# posts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView, CustomLoginView

urlpatterns = [
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("", PostListView.as_view(), name="post_list"),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Authentication URLs
    path('login/', CustomLoginView.as_view(template_name='posts/pages/authentication/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]