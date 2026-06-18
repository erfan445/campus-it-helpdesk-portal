import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.common import paginate_queryset
from .forms import TicketCommentForm, TicketCreateForm, TicketUpdateForm
from .models import Ticket
from .selectors import dashboard_statistics, filter_tickets, tickets_visible_to
from .services import add_ticket_comment, create_ticket, update_ticket


@login_required
def dashboard(request):
    stats = dashboard_statistics(request.user)
    return render(request, 'tickets/dashboard.html', stats)


@login_required
def ticket_list(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()
    category = request.GET.get('category', '').strip()

    tickets = tickets_visible_to(request.user)
    tickets = filter_tickets(tickets, query=query, status=status, priority=priority, category=category)
    page_obj = paginate_queryset(request, tickets, per_page=10)

    return render(request, 'tickets/ticket_list.html', {
        'page_obj': page_obj,
        'status_choices': Ticket.Status.choices,
        'priority_choices': Ticket.Priority.choices,
        'category_choices': Ticket.Category.choices,
        'selected': {'q': query, 'status': status, 'priority': priority, 'category': category},
    })


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(tickets_visible_to(request.user), id=ticket_id)

    if request.method == 'POST':
        form = TicketCommentForm(request.POST)
        if form.is_valid():
            add_ticket_comment(
                ticket=ticket,
                author=request.user,
                body=form.cleaned_data['body'],
                is_internal_note=form.cleaned_data['is_internal_note'],
            )
            messages.success(request, 'Note added to ticket.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketCommentForm()

    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'comment_form': form})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = create_ticket(requester=request.user, form_data=form.cleaned_data)
            messages.success(request, f'Ticket {ticket.reference} created.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketCreateForm()

    return render(request, 'tickets/ticket_form.html', {'form': form, 'page_title': 'Create Support Ticket'})


@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(tickets_visible_to(request.user), id=ticket_id)

    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = update_ticket(ticket=ticket, form=form, changed_by=request.user)
            messages.success(request, f'Ticket {ticket.reference} updated.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(request, 'tickets/ticket_form.html', {'form': form, 'page_title': 'Update Ticket'})


@login_required
def export_tickets_csv(request):
    tickets = tickets_visible_to(request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="helpdesk_ticket_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Reference', 'Subject', 'Category', 'Priority', 'Impact', 'Urgency',
        'Status', 'Requester', 'Assigned To', 'Asset', 'Location', 'Due At',
        'Created At', 'Resolved At'
    ])

    for ticket in tickets:
        writer.writerow([
            ticket.reference,
            ticket.subject,
            ticket.get_category_display(),
            ticket.get_priority_display(),
            ticket.get_impact_display(),
            ticket.get_urgency_display(),
            ticket.get_status_display(),
            ticket.requester.username,
            ticket.assigned_to.username if ticket.assigned_to else 'Unassigned',
            ticket.asset.asset_tag if ticket.asset else '',
            ticket.location,
            ticket.due_at.strftime('%Y-%m-%d %H:%M') if ticket.due_at else '',
            ticket.created_at.strftime('%Y-%m-%d %H:%M'),
            ticket.resolved_at.strftime('%Y-%m-%d %H:%M') if ticket.resolved_at else '',
        ])

    return response
