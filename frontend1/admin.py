from django.contrib import admin
from .models import CustomUser
# Register your models here.

class regAdmin(admin.ModelAdmin):
    list_display=['username','fullname','email','phone_no','password']
admin.site.register(CustomUser, regAdmin)