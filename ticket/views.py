from gc import get_objects
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Ticket, DutyRoaster
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.http import HttpResponse
from .forms import TicketCreateForm, TicketEmployeeUpdateForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def admin_or_employee_check(request):
    return request.user.is_admin or request.user.profile in request.user.profile.ticket_set.all().first().employees.all()

@login_required
def dashboard(request):
    tickets = Ticket.objects.all().order_by('-date_created')
    context = {
        'tickets': tickets
    }
    return render(request, 'ticket/dashboard.html', context)

@login_required
def ticket_create_view(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user.profile
            form.save()
            messages.success(request, "Ticket added successfully")
            return redirect('ticket:tickets')
    form = TicketCreateForm()
    context = {
        'form': form
    }
    return render(request, 'ticket/create.html', context)

class TicketUpdateView(UpdateView, LoginRequiredMixin):
    model = Ticket
    form_class = TicketEmployeeUpdateForm
    template_name = 'ticket/update.html'

    def get_success_url(self):
        return reverse('ticket:my-tickets')
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.employee != request.user.profile:
            # User is not the owner of the post, handle the permission denied case
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        messages.success(self.request, "Ticket updated successfully")
        return super().form_valid(form)
    

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(employee=request.user.profile)
    context = {
        'tickets': tickets
    }
    return render(request, 'ticket/my-tickets.html', context)


@login_required
def duty_roster_dashboard(request):
    duty_roster = DutyRoaster.objects.all()
    context = {
        'duty_roster': duty_roster
    }
    return render(request, 'ticket/roaster.html', context)
