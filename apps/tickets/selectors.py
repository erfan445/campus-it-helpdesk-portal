from django.db.models import Count, Q
from django.utils import timezone
from .models import Ticket


def tickets_visible_to(user):
    if user.is_superuser:
        return Ticket.objects.select_related('requester', 'assigned_to', 'asset').all()

    profile = getattr(user, 'profile', None)
    if profile and profile.is_support_staff():
        return Ticket.objects.select_related('requester', 'assigned_to', 'asset').all()

    return Ticket.objects.select_related('requester', 'assigned_to', 'asset').filter(requester=user)


def filter_tickets(queryset, *, query='', status='', priority='', category=''):
    if query:
        queryset = queryset.filter(
            Q(reference__icontains=query)
            | Q(subject__icontains=query)
            | Q(description__icontains=query)
            | Q(requester__username__icontains=query)
            | Q(assigned_to__username__icontains=query)
            | Q(location__icontains=query)
            | Q(asset__asset_tag__icontains=query)
            | Q(asset__name__icontains=query)
        )
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    if category:
        queryset = queryset.filter(category=category)
    return queryset


def dashboard_statistics(user):
    tickets = tickets_visible_to(user)
    now = timezone.now()
    return {
        'total': tickets.count(),
        'open': tickets.filter(status=Ticket.Status.OPEN).count(),
        'assigned': tickets.filter(status=Ticket.Status.ASSIGNED).count(),
        'in_progress': tickets.filter(status=Ticket.Status.IN_PROGRESS).count(),
        'resolved': tickets.filter(status=Ticket.Status.RESOLVED).count(),
        'critical': tickets.filter(priority=Ticket.Priority.CRITICAL).count(),
        'overdue': tickets.filter(due_at__lt=now).exclude(status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED]).count(),
        'recent': tickets[:6],
        'by_status': tickets.values('status').annotate(total=Count('id')).order_by('status'),
        'by_priority': tickets.values('priority').annotate(total=Count('id')).order_by('priority'),
    }
