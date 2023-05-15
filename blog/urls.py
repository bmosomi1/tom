from django.urls import path
from . import views

app_name = 'water'
urlpatterns = [
    path('', views.home, name='water-home'),
    #path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    #path('post/new', PostCreateView.as_view(), name='post-create'),
    #path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    #path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]