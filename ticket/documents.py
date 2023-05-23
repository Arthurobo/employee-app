from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry

from .models import Ticket


PUBLISHER_INDEX = Index('ticket_demo')


PUBLISHER_INDEX.settings(
    number_of_shards = 1,
    number_of_replicas = 1
)

@PUBLISHER_INDEX.doc_type
class TicketDocument(Document):
    id = fields.IntegerField(attr="id")
    fielddata = True

    ticket_number = fields.TextField(
        fields = {
            "raw": {
                "type": "keyword",
            }
        }
    )

   
    class Django(object):
        model = Ticket