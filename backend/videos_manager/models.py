from django.db import models
from django.contrib.auth.models import User


class YTUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    youtube_link = models.URLField(unique=True)
    subscribers_count = models.PositiveIntegerField(default=0)
    latest_video = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')
    video_link = models.URLField()
    thumbnail = models.ImageField(
        upload_to='thumbnails/', blank=True, null=True)
    duration = models.DurationField()
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    # Indicates if the video is available for download
    download = models.BooleanField(default=False)
    author = models.ForeignKey(
        YTUser, on_delete=models.CASCADE, related_name="videos_authored")
    requested_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="videos_requested")

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title
