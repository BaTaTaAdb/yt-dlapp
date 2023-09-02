from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Video, YTUser


@admin.register(YTUser)
class YTUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'latest_video', 'number_of_videos')
    search_fields = ('name', 'user_id')

    def number_of_videos(self, obj):
        return obj.videos.count()
    number_of_videos.short_description = 'Number of Videos'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'upload_date', 'views', 'video_id',
                    'download', 'ytuser', 'requested_by')
    search_fields = ('title', 'ytuser__name', 'description', 'video_id')
