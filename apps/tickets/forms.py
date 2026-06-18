from django import forms
from .models import Ticket, TicketComment


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'subject',
            'description',
            'category',
            'priority',
            'impact',
            'urgency',
            'asset',
            'location',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Explain the problem, error message, and when it started.'}),
        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'status',
            'priority',
            'assigned_to',
            'due_at',
            'resolution_summary',
        ]
        widgets = {
            'due_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'resolution_summary': forms.Textarea(attrs={'rows': 4}),
        }


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['body', 'is_internal_note']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add troubleshooting steps, user update, or internal note.'}),
        }
