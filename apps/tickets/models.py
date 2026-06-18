from django.conf import settings
from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    class Category(models.TextChoices):
        NETWORK = 'NETWORK', 'Network'
        HARDWARE = 'HARDWARE', 'Hardware'
        SOFTWARE = 'SOFTWARE', 'Software'
        ACCOUNT = 'ACCOUNT', 'Account/Login'
        SECURITY = 'SECURITY', 'Security'
        ACCESS = 'ACCESS', 'Access Request'
        OTHER = 'OTHER', 'Other'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        WAITING_USER = 'WAITING_USER', 'Waiting User'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    class Impact(models.TextChoices):
        LOW = 'LOW', 'Single user affected'
        MEDIUM = 'MEDIUM', 'Department affected'
        HIGH = 'HIGH', 'Campus/service affected'

    reference = models.CharField(max_length=20, unique=True, blank=True)
    subject = models.CharField(max_length=160)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    impact = models.CharField(max_length=20, choices=Impact.choices, default=Impact.LOW)
    urgency = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OPEN)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_tickets')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_tickets')
    asset = models.ForeignKey('assets.Asset', on_delete=models.SET_NULL, blank=True, null=True, related_name='tickets')
    location = models.CharField(max_length=120, blank=True)
    due_at = models.DateTimeField(blank=True, null=True)
    resolution_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if self.status in [self.Status.RESOLVED, self.Status.CLOSED] and self.resolved_at is None:
            self.resolved_at = timezone.now()
        if self.status not in [self.Status.RESOLVED, self.Status.CLOSED]:
            self.resolved_at = None
        super().save(*args, **kwargs)
        if is_new and not self.reference:
            self.reference = f'HD-{timezone.now().year}-{self.id:04d}'
            super().save(update_fields=['reference'])

    @property
    def is_overdue(self):
        return self.due_at is not None and self.due_at < timezone.now() and self.status not in [self.Status.RESOLVED, self.Status.CLOSED]

    def __str__(self):
        return f'{self.reference or "New Ticket"} - {self.subject}'


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    is_internal_note = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        note_type = 'Internal note' if self.is_internal_note else 'Comment'
        return f'{note_type} on {self.ticket.reference}'


class TicketStatusHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='status_history')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    old_status = models.CharField(max_length=30, blank=True)
    new_status = models.CharField(max_length=30)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f'{self.ticket.reference}: {self.old_status} -> {self.new_status}'
