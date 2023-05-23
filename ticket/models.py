from django.db import models
import random
from django.urls import reverse


class Ticket(models.Model):
    # The user that actually opened the ticket
    user = models.ForeignKey('accounts.Profile', blank=True, null=True, on_delete=models.SET_NULL, related_name='ticket_user')
    employee = models.ForeignKey('accounts.Profile', blank=True, null=True, on_delete=models.SET_NULL, related_name='ticket_employee')
    ticket_number = models.CharField(max_length=30)
    description = models.TextField()
    resolution_end_date = models.DateTimeField(blank=True, null=True)
    finalized = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ticket_number)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            random_numbers = random.randrange(10**9, 10**10)
            self.ticket_number = random_numbers
        super().save(*args, **kwargs)

    def get_employee_update_url(self):
        return reverse('ticket:ticket-update', kwargs={'pk': self.pk})


class DutyRoaster(models.Model):
    ticket = models.ForeignKey("ticket.Ticket", blank=True, null=True, on_delete=models.CASCADE)
    employee = models.ForeignKey('accounts.Profile', blank=True, null=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    availability_status = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
