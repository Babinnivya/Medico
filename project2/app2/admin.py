from django.contrib import admin
from .models import medical
# Register your models here.
class MedicalAdmin(admin.ModelAdmin):
    list_display=['name','quantity','price','expirydate']


admin.site.register(medical,MedicalAdmin)