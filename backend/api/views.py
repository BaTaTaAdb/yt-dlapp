from rest_framework import generics, status
from rest_framework.response import Response
from videos_manager.models import Video, YTUser
from .serializers.video_serializer import VideoSerializer
from .serializers.ytuser_serializer import YTUserSerializer
from .serializers.video_link_serialiazer import VideoLinkSerializer
from videos_manager.downloader import *
from datetime import timedelta
import traceback


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
        user = serializer.validated_data['user']

        # Parse the link to extract video and user information
        yt = create_yt(link)

        # Check if the video link already exists in the database
        if Video.objects.filter(video_id=yt.video_id).exists():
            return Response({"error": "Video already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # If channel id already exists, then fetch from youtube
        ytuser, created = YTUser.objects.get_or_create(
            user_id=yt.channel_id, defaults={'name': yt.author})

        if created:
            ytuser.latest_video = get_latest_video(yt.channel_url)
            ytuser.save()

        # Create a new Video instance with the provided link and associated YTUser
        video = Video(ytuser=ytuser, title=yt.title,
                      description=yt.description, video_id=yt.video_id, duration=timedelta(
                          seconds=yt.length), views=yt.views, requested_by=user)

        yt = create_yt_from_id(yt.video_id)
        if get_max_res(video_streams=get_video_streams(yt),
                       audio_streams=get_audio_streams(yt),
                       video_id=yt.video_id,
                       file_name=remove_special_characters(yt.title)):
            video.download = True
            video.save()
            return Response({"message": "Video and YTUser created successfully"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Error while downloading video"}, status=status.HTTP_400_BAD_REQUEST)
