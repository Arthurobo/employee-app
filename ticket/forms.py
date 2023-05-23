from .models import Ticket

from accounts.models import Profile, Account

from django import forms 


class TicketCreateForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
            label='Select Employee',
            widget=forms.Select(attrs={'class': 'form-control'}),
            queryset=Profile.objects.all(),
        )
    class Meta:
        model = Ticket
        fields = ['employee', 'description']


class TicketEmployeeUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['description', 'finalized',]