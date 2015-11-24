"""
API methods for module level data.
"""

import datetime
from django.conf import settings
from django.utils.timezone import make_aware, utc
from rest_framework import generics

from analytics_data_api.learner_analytics.v0.models import RosterEntry
from analytics_data_api.learner_analytics.v0.serializers import LearnerSerializer


class CourseViewMixin(object):

    COURSE_ID_PATTERN = r'(?P<course_id>[^/+]+[/+][^/+]+[/+][^/]+)'
    course_id = None

    def get(self, request, *args, **kwargs):
        # TODO: validate course_id
        self.course_id = request.QUERY_PARAMS.get('course_id')
        return super(CourseViewMixin, self).get(request, *args, **kwargs)


class LearnersListView(CourseViewMixin, generics.ListAPIView):
    """
    Get the counts of users and views for a video.

    **Example Request**

        GET /api/v0/videos/{video_id}/timeline/

    **Response Values**

        Returns viewing data for each segment of a video.  For each segment,
        the collection contains the following data.

            * segment: The order of the segment in the video timeline.
            * num_users: The number of unique users who viewed this segment.
            * num_views: The number of views for this segment.
            * created: The date the segment data was computed.

    **Parameters**

        You can specify the activity type for which you want to get the count.

        course_id -- Course ID

    """

    serializer_class = LearnerSerializer
    allow_empty = False

    def get_queryset(self):
        roster = RosterEntry.search().filter('term', course_id=self.course_id).execute()
        return roster


# TODO: figure out if we can ue RetrieveAPIView instead (error w/ pk not being defined) -- AN-6291
class LearnerView(CourseViewMixin, generics.ListAPIView):
    """
    Get the counts of users and views for a video.

    **Example Request**

        GET /api/v0/videos/{video_id}/timeline/

    **Response Values**

        Returns viewing data for each segment of a video.  For each segment,
        the collection contains the following data.

            * segment: The order of the segment in the video timeline.
            * num_users: The number of unique users who viewed this segment.
            * num_views: The number of views for this segment.
            * created: The date the segment data was computed.

    **Parameters**

        You can specify the activity type for which you want to get the count.

        course_id -- Course ID

    """
    serializer_class = LearnerSerializer
    allow_empty = False
    username = None

    def get(self, request, *args, **kwargs):
        self.username = self.kwargs.get('username')
        return super(LearnerView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        roster = RosterEntry.search().filter('term', course_id=self.course_id)\
            .query('match', username=self.username).execute()
        return roster
