from elasticsearch_dsl import connections, Index, DocType, String

connections.connections.create_connection(hosts=['https://search-dev-edx-insights-7nxf4fiyp47ftvhzvruauwswqa.us-east-1.es.amazonaws.com:8443/'])

roster = Index('roster_1_1')
@roster.doc_type
class RosterEntry(DocType):
     username = String(index='not_analyzed')
     class Meta:
          doc_type = 'roster_entry'
