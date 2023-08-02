from django.contrib import admin
from descriptions.models import Description

# Register your models here.
from .models import Description
 
@admin.register(Description)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
Description._meta.get_fields()]
