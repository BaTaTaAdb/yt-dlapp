from django.urls import path
from .views import VideoListCreateView, VideoRetrieveUpdateDestroyView, VideoLinkCreateView, VideoDownloadView

urlpatterns = [
    path('videos/link/', VideoLinkCreateView.as_view(), name='video-link-create'),
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('videos/<str:video_id>/', VideoRetrieveUpdateDestroyView.as_view(),
         name='video-retrieve-update-destroy'),
    path('videos/download/<str:video_id>/',
         VideoDownloadView.as_view(), name='video-download'),
]
