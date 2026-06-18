from datetime import timedelta
from django.utils import timezone
from .models import Ticket, TicketComment, TicketStatusHistory


SLA_HOURS_BY_PRIORITY = {
    Ticket.Priority.CRITICAL: 4,
    Ticket.Priority.HIGH: 8,
    Ticket.Priority.MEDIUM: 24,
    Ticket.Priority.LOW: 72,
}


def calculate_due_date(priority):
    hours = SLA_HOURS_BY_PRIORITY.get(priority, 24)
    return timezone.now() + timedelta(hours=hours)


def create_ticket(*, requester, form_data):
    ticket = Ticket(**form_data)
    ticket.requester = requester
    ticket.due_at = calculate_due_date(ticket.priority)
    ticket.save()
    TicketStatusHistory.objects.create(
        ticket=ticket,
        changed_by=requester,
        old_status='',
        new_status=ticket.status,
    )
    return ticket


def update_ticket(*, ticket, form, changed_by):
    old_status = ticket.status
    updated_ticket = form.save()
    if old_status != updated_ticket.status:
        TicketStatusHistory.objects.create(
            ticket=updated_ticket,
            changed_by=changed_by,
            old_status=old_status,
            new_status=updated_ticket.status,
        )
    return updated_ticket


def add_ticket_comment(*, ticket, author, body, is_internal_note=False):
    return TicketComment.objects.create(
        ticket=ticket,
        author=author,
        body=body,
        is_internal_note=is_internal_note,
    )
