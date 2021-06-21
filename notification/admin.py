from django.contrib import admin
from  .models import Notification

# Register your models here.

# admin.site.register(Notification)

@admin.register(Notification)
class NotifificationAdmin(admin.ModelAdmin):
    list_display = ['to_user', 'notification_type', 'is_read','created_by', 'create_date', 'message']
    