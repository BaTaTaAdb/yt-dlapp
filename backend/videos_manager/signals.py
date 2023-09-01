from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Video, YTUser
from .downloader import *


@receiver(post_save, sender=Video)
def set_user_on_video_create(sender, instance: Video, created, **kwargs):
    if created and not instance.ytuser:  # Check if a new record was created and ytuser is not set
        yt = create_yt(instance.video_link)

        # If channel id already exists, then set Video.ytuser and fetch from youtube
        ytuser, created = YTUser.objects.get_or_create(
            user_id=yt.channel_id, defaults={'name': yt.author})

        if created:
            ytuser.latest_video = get_latest_video(yt.channel_url)
            ytuser.save()

        instance.ytuser = ytuser
        get_max_res(yt)
        instance.save()
