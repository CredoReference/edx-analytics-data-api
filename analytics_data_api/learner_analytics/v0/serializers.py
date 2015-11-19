from rest_framework import serializers


class LearnerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    enrollment_mode = serializers.CharField(max_length=200)
    course_id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
