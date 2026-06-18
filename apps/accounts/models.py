from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    class Role(models.TextChoices):
        REQUESTER = 'REQUESTER', 'Requester'
        TECHNICIAN = 'TECHNICIAN', 'Technician'
        HELP_DESK_MANAGER = 'HELP_DESK_MANAGER', 'Help Desk Manager'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.REQUESTER)
    department = models.CharField(max_length=80, blank=True)
    phone_extension = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_support_staff(self):
        return self.role in [self.Role.TECHNICIAN, self.Role.HELP_DESK_MANAGER]

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'
