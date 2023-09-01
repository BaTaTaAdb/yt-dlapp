from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'views', 'download', 'author')
    search_fields = ('title', 'author__username')
