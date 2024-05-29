from django.contrib import admin
from .models import Hist

# Register your models here.
@admin.register(Hist)
class HistAdmin(admin.ModelAdmin):
    list_display = ('text', 'label', 'prob')