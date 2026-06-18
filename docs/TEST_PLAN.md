# Test Plan

## Manual tests

1. Login as `student1`.
2. Create a new support ticket.
3. Confirm the ticket receives a reference number.
4. Login as `technician1`.
5. Open the ticket list and assign/update the ticket.
6. Add a troubleshooting comment.
7. Change ticket status to resolved.
8. Export CSV and verify ticket data appears.
9. Open assets page and link an asset to a ticket.

## Automated tests

Run:

```bash
python manage.py test
```

Current tests check:

- User profile creation
- Asset model output
- Ticket creation service
- Ticket reference generation
- Status history creation
- Ticket visibility rules
