from django.contrib import admin
from user.models import User

# Register your models here.
from .models import User
 
@admin.register(User)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
User._meta.get_fields()]
