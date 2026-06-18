# Database Schema Summary

## UserProfile

Extends Django users with helpdesk role, department, extension, and job title.

## Asset

Represents a device or IT asset.

Important fields:

- asset_tag
- name
- category
- status
- assigned_to
- location
- warranty_expiry

## Ticket

Represents a support request.

Important fields:

- reference
- subject
- description
- category
- priority
- impact
- urgency
- status
- requester
- assigned_to
- asset
- location
- due_at
- resolution_summary

## TicketComment

Stores troubleshooting comments and internal notes.

## TicketStatusHistory

Stores ticket status changes for basic audit tracking.
