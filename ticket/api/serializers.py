from rest_framework import serializers
from ticket.models import Ticket
from ticket.documents import TicketDocument
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer


class TicketListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = '__all__'


class TicketCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = ['employee', 'description', 'ticket_number']
		


# Note Serializer for ElasticSearch
class TicketDocumentSerializer(DocumentSerializer):
    class Meta(object):
        """ Meta Options """
        model = Ticket.objects.all()
        document = TicketDocument
        fields = '__all__'
     
        def get_location(self, obj):
            """ Represents location Value """
            try:
                return obj.location.to_dict()
            except:
                return {}