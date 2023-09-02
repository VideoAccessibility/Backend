from django.contrib import admin
from questions.models import Question

# Register your models here.
from .models import Question
 
@admin.register(Question)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
Question._meta.get_fields()]
