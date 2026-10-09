---
name: supplier-reminders
description: Procedure to prepare reminders to
  suppliers with blocked orders. Use it when you are
  asked to chase stalled or overdue orders.
---

# Procedure

1. Search the orders with search_orders(status="blocked",
   min_days=7): below 7 days you do not send a reminder.
2. For each order fetch the contacts with get_supplier().
   If the email is missing, do not make up contact details:
   flag the case to an operator in the final summary.
3. Prepare each draft with prepare_reminder() starting
   from reminder_template.md, in this folder. Beyond
   30 days of block, cite the contract reference
   and ask for a precise unblock date.
4. Close with the summary: drafts created, with id, and
   cases that require an operator.
