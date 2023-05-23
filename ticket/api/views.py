from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

""" Elasticsearch Imports """
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
    OrderingFilterBackend,
)

from accounts.models import Account, Profile
from ticket.models import Ticket
from ticket.documents import TicketDocument
from .serializers import (TicketListSerializer, TicketCreateSerializer, TicketDocumentSerializer
                        )


class TicketAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Ticket.objects.all()
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer
        else:
            return TicketListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        message = 'Success'
        status_code = 200
        return Response({'status': status_code, 'message': message, 'data': data}, status=status_code)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # random_numbers = random.randrange(10**9, 10**10)
            # ticket_number = random_numbers
            serializer.save(user=self.request.user.profile)
            message = 'Data saved successfully'
            status_code = 201
            data = serializer.data
            return Response({'status': status_code, 'message': message, 'data': data}, status=status_code)
        else:
            message = 'Data could not be saved'
            status_code = 400
            return Response({'status': status_code, 'message': message, 'errors': serializer.errors}, status=status_code)
        





# ElasticSearch Serializer Search View
class TicketDocumentView(DocumentViewSet):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    document = TicketDocument
    serializer_class = TicketDocumentSerializer
    lookup_field = "title"
    fielddata = True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = (
        "ticket_number",
        "description",
    )

    multi_match_search_fields = (
        "ticket_number",
        "description",
    )

    filter_fields = {
        "ticket_number": "ticket_number",
        "description": "description",
    }

    ordering_fields = {
        'id': None,
    }

    ordering = ("id",)