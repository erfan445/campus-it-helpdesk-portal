from django.contrib.auth.models import User
from django.test import TestCase
from apps.accounts.models import UserProfile
from apps.tickets.models import Ticket
from apps.tickets.services import create_ticket
from apps.tickets.selectors import tickets_visible_to


class TicketSelectorTests(TestCase):
    def setUp(self):
        self.requester = User.objects.create_user(username='requester', password='pass12345')
        self.other_user = User.objects.create_user(username='other', password='pass12345')
        self.tech = User.objects.create_user(username='tech', password='pass12345')
        self.tech.profile.role = UserProfile.Role.TECHNICIAN
        self.tech.profile.save()
        create_ticket(
            requester=self.requester,
            form_data={
                'subject': 'Keyboard not working',
                'description': 'Several keys do not respond.',
                'category': Ticket.Category.HARDWARE,
                'priority': Ticket.Priority.LOW,
                'impact': Ticket.Impact.LOW,
                'urgency': Ticket.Priority.LOW,
                'asset': None,
                'location': 'Lab',
            },
        )

    def test_requester_only_sees_own_tickets(self):
        self.assertEqual(tickets_visible_to(self.requester).count(), 1)
        self.assertEqual(tickets_visible_to(self.other_user).count(), 0)

    def test_technician_sees_all_tickets(self):
        self.assertEqual(tickets_visible_to(self.tech).count(), 1)
