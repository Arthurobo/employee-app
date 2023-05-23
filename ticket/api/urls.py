from django.urls import path
from .views import TicketAPIView, TicketDocumentView

app_name = 'ticket_api'


urlpatterns = [
    path('', TicketAPIView.as_view(), name='tickets'),
    path('search/' , TicketDocumentView.as_view({'get': 'list'})),
]