from datetime import timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import UserProfile
from apps.assets.models import Asset
from apps.tickets.models import Ticket
from apps.tickets.services import add_ticket_comment, create_ticket


class Command(BaseCommand):
    help = 'Create realistic demo users, assets, and tickets for the helpdesk portal.'

    def _user(self, username, password, email, role, department='', job_title=''):
        user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
        user.set_password(password)
        user.email = email
        if username == 'admin':
            user.is_staff = True
            user.is_superuser = True
        user.save()
        user.profile.role = role
        user.profile.department = department
        user.profile.job_title = job_title
        user.profile.save()
        return user

    def handle(self, *args, **options):
        admin = self._user('admin', 'admin12345', 'admin@example.com', UserProfile.Role.HELP_DESK_MANAGER, 'IT Services', 'Help Desk Manager')
        tech1 = self._user('technician1', 'tech12345', 'tech1@example.com', UserProfile.Role.TECHNICIAN, 'IT Services', 'Support Technician')
        tech2 = self._user('technician2', 'tech12345', 'tech2@example.com', UserProfile.Role.TECHNICIAN, 'Network Team', 'Network Technician')
        student = self._user('student1', 'user12345', 'student1@example.com', UserProfile.Role.REQUESTER, 'Software Engineering', 'Student')
        staff = self._user('staff1', 'user12345', 'staff1@example.com', UserProfile.Role.REQUESTER, 'Library', 'Library Assistant')

        assets = [
            {'asset_tag': 'EMU-LAP-001', 'name': 'Dell Latitude 5420', 'category': Asset.Category.LAPTOP, 'status': Asset.Status.ACTIVE, 'serial_number': 'DL5420-1182', 'location': 'Library', 'assigned_to': staff},
            {'asset_tag': 'EMU-PRN-014', 'name': 'HP LaserJet M404', 'category': Asset.Category.PRINTER, 'status': Asset.Status.IN_REPAIR, 'serial_number': 'HPM404-9921', 'location': 'Admin Office', 'assigned_to': None},
            {'asset_tag': 'EMU-SW-003', 'name': 'Cisco 2960 Switch', 'category': Asset.Category.NETWORK, 'status': Asset.Status.ACTIVE, 'serial_number': 'C2960-2301', 'location': 'Network Rack A', 'assigned_to': None},
            {'asset_tag': 'EMU-DESK-020', 'name': 'Lenovo ThinkCentre', 'category': Asset.Category.DESKTOP, 'status': Asset.Status.ACTIVE, 'serial_number': 'LTC-7781', 'location': 'Computer Lab 2', 'assigned_to': student},
        ]

        created_assets = {}
        for item in assets:
            asset, _ = Asset.objects.update_or_create(asset_tag=item['asset_tag'], defaults=item)
            created_assets[asset.asset_tag] = asset

        demo_tickets = [
            {
                'requester': staff,
                'assigned_to': tech2,
                'form_data': {
                    'subject': 'Wi-Fi disconnects every few minutes in library',
                    'description': 'The library laptop loses Wi-Fi connection repeatedly. Other users reported weaker signal near the back desk.',
                    'category': Ticket.Category.NETWORK,
                    'priority': Ticket.Priority.HIGH,
                    'impact': Ticket.Impact.MEDIUM,
                    'urgency': Ticket.Priority.HIGH,
                    'asset': created_assets['EMU-LAP-001'],
                    'location': 'Library back desk',
                },
                'status': Ticket.Status.IN_PROGRESS,
                'note': 'Checked IP configuration and DNS. Next step is to test access point signal strength near the back desk.',
            },
            {
                'requester': student,
                'assigned_to': tech1,
                'form_data': {
                    'subject': 'Cannot sign in to Microsoft 365 account',
                    'description': 'User reports password reset loop and cannot access email from laptop or phone.',
                    'category': Ticket.Category.ACCOUNT,
                    'priority': Ticket.Priority.MEDIUM,
                    'impact': Ticket.Impact.LOW,
                    'urgency': Ticket.Priority.MEDIUM,
                    'asset': created_assets['EMU-DESK-020'],
                    'location': 'Computer Lab 2',
                },
                'status': Ticket.Status.ASSIGNED,
                'note': 'Verified username format and advised user to complete MFA verification.',
            },
            {
                'requester': staff,
                'assigned_to': tech1,
                'form_data': {
                    'subject': 'Printer stuck in offline mode',
                    'description': 'Office printer appears offline from two Windows computers even after restart.',
                    'category': Ticket.Category.HARDWARE,
                    'priority': Ticket.Priority.LOW,
                    'impact': Ticket.Impact.LOW,
                    'urgency': Ticket.Priority.LOW,
                    'asset': created_assets['EMU-PRN-014'],
                    'location': 'Admin Office',
                },
                'status': Ticket.Status.RESOLVED,
                'note': 'Reinstalled printer driver and cleared old print queue. Test page printed successfully.',
            },
            {
                'requester': student,
                'assigned_to': tech2,
                'form_data': {
                    'subject': 'Suspicious email asking for password confirmation',
                    'description': 'User received an email claiming the university mailbox will close unless password is confirmed.',
                    'category': Ticket.Category.SECURITY,
                    'priority': Ticket.Priority.CRITICAL,
                    'impact': Ticket.Impact.MEDIUM,
                    'urgency': Ticket.Priority.CRITICAL,
                    'asset': None,
                    'location': 'Student email account',
                },
                'status': Ticket.Status.WAITING_USER,
                'note': 'User was advised not to click the link. Recommended password change and MFA review.',
            },
        ]

        for item in demo_tickets:
            existing = Ticket.objects.filter(subject=item['form_data']['subject']).first()
            if existing:
                continue
            ticket = create_ticket(requester=item['requester'], form_data=item['form_data'])
            ticket.assigned_to = item['assigned_to']
            ticket.status = item['status']
            if item['status'] == Ticket.Status.RESOLVED:
                ticket.resolution_summary = item['note']
            if item['status'] == Ticket.Status.WAITING_USER:
                ticket.due_at = timezone.now() - timedelta(hours=2)
            ticket.save()
            add_ticket_comment(ticket=ticket, author=item['assigned_to'], body=item['note'], is_internal_note=False)

        self.stdout.write(self.style.SUCCESS('Demo helpdesk data created successfully.'))
        self.stdout.write('Admin: admin / admin12345')
        self.stdout.write('Technician: technician1 / tech12345')
        self.stdout.write('Requester: student1 / user12345')
