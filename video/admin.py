from django.contrib import admin
from video.models import Video

# Register your models here.
from .models import Video
 
@admin.register(Video)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
Video._meta.get_fields()]
