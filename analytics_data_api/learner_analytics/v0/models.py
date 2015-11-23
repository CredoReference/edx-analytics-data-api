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


class Engagement(models.Model):
    """User interactions with entities within the courseware."""

    course_id = models.CharField(db_index=True, max_length=255)
    username = models.CharField(max_length=30)
    date = models.DateTimeField()
    entity_type = models.CharField(max_length=10)
    entity_id = models.CharField(max_length=255)
    event = models.CharField(max_length=30)
    count = models.IntegerField()

    class Meta(object):
        db_table = 'engagement'

class EngagementMetricRanges(models.Model):
    """User interactions with entities within the courseware."""

    course_id = models.CharField(db_index=True, max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    metric = models.CharField(max_length=50)
    range_type = models.CharField(max_length=50)
    high_value = models.FloatField()
    low_value = models.FloatField()

    class Meta(object):
        db_table = 'engagement_metric_ranges'
