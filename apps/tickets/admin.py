from django.contrib import admin
from .models import Ticket, TicketComment, TicketStatusHistory


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0


class TicketStatusHistoryInline(admin.TabularInline):
    model = TicketStatusHistory
    extra = 0
    readonly_fields = ('changed_at',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('reference', 'subject', 'category', 'priority', 'status', 'requester', 'assigned_to', 'due_at', 'created_at')
    list_filter = ('category', 'priority', 'status', 'impact', 'created_at')
    search_fields = ('reference', 'subject', 'description', 'requester__username', 'assigned_to__username', 'location')
    readonly_fields = ('reference', 'created_at', 'updated_at', 'resolved_at')
    inlines = [TicketCommentInline, TicketStatusHistoryInline]


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'is_internal_note', 'created_at')
    list_filter = ('is_internal_note', 'created_at')
    search_fields = ('body', 'ticket__reference', 'author__username')


@admin.register(TicketStatusHistory)
class TicketStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('new_status', 'changed_at')
