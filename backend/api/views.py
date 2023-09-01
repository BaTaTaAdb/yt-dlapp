from rest_framework import generics, status
from rest_framework.response import Response
from videos_manager.models import Video, YTUser
from .serializers.video_serializer import VideoSerializer
from .serializers.ytuser_serializer import YTUserSerializer
from .serializers.video_link_serialiazer import VideoLinkSerializer


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

        # Create a new Video instance with the provided link
        video = Video(video_link=link)
        video.save()  # This will trigger the post_save signal

        return Response({"message": "Video and YTUser created successfully"}, status=status.HTTP_201_CREATED)
