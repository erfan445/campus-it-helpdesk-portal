# Architecture Notes

This project uses a small modular Django structure.

## Apps

### accounts

Stores a profile for each Django user. The profile adds a helpdesk role:

- Requester
- Technician
- Help Desk Manager

### assets

Stores IT inventory such as laptops, printers, desktops, and network devices. Tickets can be linked to assets so troubleshooting history is easier to follow.

### tickets

Stores the main support workflow:

- Ticket
- TicketComment
- TicketStatusHistory

The tickets app also includes service functions and selectors.

## Why services and selectors are included

Small projects often put all logic directly inside views. This project separates logic a bit more professionally:

- `services.py` changes data or creates records.
- `selectors.py` reads/filter data for views.
- `views.py` handles request/response.

This makes the code easier to test and review.
