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
    # This will be one of "problem", "video" or "forum"
    entity_type = models.CharField(max_length=10)
    # For problems this will be the usage key, for videos it will be the html encoded module ID,
    # for forums it will be the commentable_id
    entity_id = models.CharField(max_length=255)
    # A description of what interaction occurred.
    event = models.CharField(max_length=30)
    # The number of times the user interacted with this entity in this way on this day.
    count = models.IntegerField()

    class Meta(object):
        db_table = 'engagement'


class EngagementMetricRanges(models.Model):
    """Engagement metric ranges"""

    course_id = models.CharField(db_index=True, max_length=255)
    start_date = models.DateTimeField()
    # This is a left-closed interval, so no data from the end_date is included in the analysis.
    end_date = models.DateTimeField()
    metric = models.CharField(max_length=50)
    range_type = models.CharField(max_length=50)
    # Also a left-closed interval, so any metric whose value is equal to the high_value
    # is not included in this range.
    high_value = models.FloatField()
    low_value = models.FloatField()

    class Meta(object):
        db_table = 'engagement_metric_ranges'
