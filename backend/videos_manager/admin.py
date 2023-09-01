from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Video, YTUser


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'views',
                    'download', 'author', 'requested_by')
    search_fields = ('title', 'author__username', 'description')


@admin.register(YTUser)
class YTUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'youtube_link',
                    'subscribers_count', 'latest_video')
    search_fields = ('name', 'youtube_link')
