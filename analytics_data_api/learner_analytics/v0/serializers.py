from rest_framework import serializers

from analytics_data_api.learner_analytics.v0.constants import (
    engagement_entity_types, engagement_events)

class BaseLearnerSerializer(serializers.Serializer):
    username = serializers.CharField()
    enrollment_mode = serializers.CharField()
    course_id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    segments = serializers.Field(source='segments')

    # TODO: why can't this be blank?
    # cohort = serializers.CharField(allow_none=True)
    # TODO: add these fields
    # enrollment_date
    # last_updated

    engagement = serializers.SerializerMethodField('get_engagement')

    def get_engagement(self, obj):
        """
        TODO: add docs
        Engagement payload...
        """
        engagement = {}
        for entity_type in engagement_entity_types.ALL:
            for event in engagement_events.EVENTS[entity_type]:
                metric = '{0}_{1}'.format(entity_type, event)
                engagement[metric] = getattr(obj, metric, 0)

        return engagement


class LearnerSerializer(BaseLearnerSerializer):
    pass
