from django.db import models
from unsc.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Notification(models.Model):

    CHOICES = [('INDIVIDUAL','INDIVIDUAL'), ('ENTITY','ENTITY')]
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    extra_id = models.CharField(max_length=20, null=True, blank=True) #make this the same as the UNList id
    create_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="from_user", on_delete=CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-create_date']