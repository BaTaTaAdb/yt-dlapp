from django.db import models
from django.contrib.auth.models import User


class YTUser(models.Model):
    """
    Represents a YouTube user or channel.

    Attributes:
    - name: The name of the YouTube user or channel.
    - user_id: The id of YouTube user's channel. Ensures uniqueness.    
    - latest_video: The link to the most recent video uploaded by the user.
    - latest_downloaded_video: ForeignKey to a Video object
    """
    name = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)
    latest_video = models.URLField(blank=True, null=True)
    latest_downloaded_video = models.ForeignKey(
        "Video", on_delete=models.SET_NULL,
        related_name='downloaded_by_users',
        blank=True, null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    """
    Represents a video, potentially from a YouTube user.

    Attributes:
    - title: The title of the video.
    - description: A brief description or summary of the video.
    - upload_date: The date and time when the video was uploaded.
    - video_file: The actual video file, stored in the 'videos/' directory.
    - video_id: The id of the video on YouTube.
    - thumbnail: An image representing the video, stored in the 'thumbnails/' directory.
    - duration: The total length or runtime of the video.
    - views: The number of times the video has been viewed.
    - download: A flag indicating if the video is available for download.
    - ytuser: A reference to the YouTube user who authored or uploaded the video.
    - requested_by: A reference to the Django user who requested this video to be added.
    - accessed_by: A referente to the Django users who have access to this video.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(blank=True, null=True)
    video_id = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/', blank=True, null=True)
    duration = models.DurationField()
    views = models.PositiveIntegerField(default=0)
    # Indicates if the video is available for download
    download = models.BooleanField(default=False)
    ytuser = models.ForeignKey(
        YTUser, on_delete=models.CASCADE, related_name="videos", null=True, blank=True)
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="videos_requested")
    accessed_by = models.ManyToManyField(User, related_name="videos_accessed")

    def __str__(self):
        return self.title
