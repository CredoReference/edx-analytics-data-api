from django.conf import settings
from django.db import models
from elasticsearch_dsl import connections, Index, DocType, String

connections.connections.create_connection(hosts=[settings.ELASTICSEARCH_LEARNERS_HOST])

roster = Index(settings.ELASTICSEARCH_LEARNERS_INDEX)
@roster.doc_type
class RosterEntry(DocType):
     username = String(index='not_analyzed')
     class Meta:
          doc_type = 'roster_entry'
