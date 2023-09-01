from rest_framework import generics, status
from rest_framework.response import Response
from videos_manager.models import Video, YTUser
from .serializers.video_serializer import VideoSerializer
from .serializers.ytuser_serializer import YTUserSerializer
from .serializers.video_link_serialiazer import VideoLinkSerializer
from videos_manager.downloader import *


class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class YTUserCreateView(generics.ListCreateAPIView):
    queryset = YTUser.objects.all()
    serializer_class = YTUserSerializer


class VideoLinkCreateView(generics.CreateAPIView):
    serializer_class = VideoLinkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        link = serializer.validated_data['link']

        # Parse the link to extract video and user information
        yt = create_yt(link)

        # If channel id already exists, then fetch from youtube
        ytuser, created = YTUser.objects.get_or_create(
            user_id=yt.channel_id, defaults={'name': yt.author})

        if created:
            ytuser.latest_video = get_latest_video(yt.channel_url)
            ytuser.save()

        # Create a new Video instance with the provided link and associated YTUser
        video = Video(video_link=link, ytuser=ytuser)
        video.save()  # This will trigger the post_save signal if you have one

        return Response({"message": "Video and YTUser created successfully"}, status=status.HTTP_201_CREATED)
