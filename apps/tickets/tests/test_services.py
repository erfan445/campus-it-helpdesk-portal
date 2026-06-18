from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from apps.tickets.models import Ticket, TicketStatusHistory
from apps.tickets.services import calculate_due_date, create_ticket


class TicketServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='StrongPass123')

    def test_due_date_is_created_from_priority(self):
        due_at = calculate_due_date(Ticket.Priority.CRITICAL)
        self.assertGreater(due_at, timezone.now())

    def test_create_ticket_generates_reference_and_history(self):
        ticket = create_ticket(
            requester=self.user,
            form_data={
                'subject': 'Laptop cannot connect to Wi-Fi',
                'description': 'Connection drops after login.',
                'category': Ticket.Category.NETWORK,
                'priority': Ticket.Priority.HIGH,
                'impact': Ticket.Impact.LOW,
                'urgency': Ticket.Priority.HIGH,
                'asset': None,
                'location': 'Library',
            },
        )
        self.assertTrue(ticket.reference.startswith('HD-'))
        self.assertEqual(TicketStatusHistory.objects.filter(ticket=ticket).count(), 1)
