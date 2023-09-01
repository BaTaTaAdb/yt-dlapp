from django.urls import path
from .views import VideoListCreateView, VideoRetrieveUpdateDestroyView, VideoLinkCreateView

urlpatterns = [
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoRetrieveUpdateDestroyView.as_view(),
         name='video-retrieve-update-destroy'),
    path('videos/link/', VideoLinkCreateView.as_view(), name='video-link-create'),
]
