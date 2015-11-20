from rest_framework import serializers


class LearnerSerializer(serializers.Serializer):
    username = serializers.CharField()
    enrollment_mode = serializers.CharField()
    course_id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    segments = serializers.Field(source='segments')

    # TODO: why can't this be blank?
    # cohort = serializers.CharField(allow_none=True)
