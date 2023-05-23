from django.urls import path
from .views import dashboard, duty_roster_dashboard, my_tickets, ticket_create_view, TicketUpdateView

app_name = 'ticket'


urlpatterns = [
    path('tickets/', dashboard, name='tickets'),
    path('tickets/create/', ticket_create_view, name='ticket-create-view'),
    path('tickets/update/<int:pk>/', TicketUpdateView.as_view(), name='ticket-update'),
    path('roaster/', duty_roster_dashboard, name='roaster'),
    path('my-tickets/', my_tickets, name='my-tickets')
]