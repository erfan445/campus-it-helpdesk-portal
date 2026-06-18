document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('.overdue-row');
    rows.forEach((row) => {
        row.title = 'This ticket is past its due date.';
    });
});
