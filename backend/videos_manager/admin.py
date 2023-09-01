from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Video, YTUser


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'views',
                    'download', 'ytuser', 'requested_by')
    search_fields = ('title', 'ytuser__username', 'description')


@admin.register(YTUser)
class YTUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'latest_video', 'videos')
    search_fields = ('name', 'user_id', 'videos')
