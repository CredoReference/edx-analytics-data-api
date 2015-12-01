"""
API methods for module level data.
"""
from rest_framework import generics

from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from analytics_data_api.v0.exceptions import (
    CourseKeyMalformedError,
    CourseNotSpecifiedError,
    LearnerNotFoundError,
    ParameterValueError,
)
from analytics_data_api.constants import learner
from analytics_data_api.v0.models import RosterEntry
from analytics_data_api.v0.serializers import ElasticsearchDSLSearchSerializer, LearnerSerializer
from analytics_data_api.v0.views.utils import split_query_argument


class CourseViewMixin(object):
    """
    Captures the course_id query arg and validates it.
    """

    course_id = None

    def get(self, request, *args, **kwargs):
        # TODO: We should check that the course_id exists at all in
        # the data store.
        self.course_id = request.QUERY_PARAMS.get('course_id', None)
        if not self.course_id:
            raise CourseNotSpecifiedError()
        try:
            CourseKey.from_string(self.course_id)
        except InvalidKeyError:
            raise CourseKeyMalformedError(course_id=self.course_id)
        return super(CourseViewMixin, self).get(request, *args, **kwargs)


class LearnerView(CourseViewMixin, generics.RetrieveAPIView):
    """
    Get a particular student's data for a particular course.

    **Example Request**

        GET /api/v0/learners/{username}/?course_id={course_id}

    **Response Values**

        Returns viewing data for each segment of a video.  For each segment,
        the collection contains the following data.

            * segment: The order of the segment in the video timeline.
            * num_users: The number of unique users who viewed this segment.
            * num_views: The number of views for this segment.
            * created: The date the segment data was computed.

        Returns the user metadata and engagement data:

            * username: User name.
            * enrollment_mode: Enrollment mode (e.g. "honor).
            * name: User name.
            * email: User email.
            * segments: Classification for this course based on engagement, (e.g. "has_potential").
            * engagements: Summary of engagement events for a time span.
                * videos_viewed: Number of times a video was played.
                * problems_completed: Unique number of problems completed.
                * problems_attempted: Unique number of problems attempted.
                * problem_attempts: Number of attempts of problems.
                * discussions_contributed: Number of discussions (e.g. forum posts).

    **Parameters**

        You can specify the course ID for which you want data.

        course_id -- The course within which user data is requested.

    """
    serializer_class = LearnerSerializer
    username = None
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        self.username = self.kwargs.get('username')
        return super(LearnerView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return RosterEntry.get_course_user(self.course_id, self.username)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        if len(queryset) == 1:
            return queryset[0]
        raise LearnerNotFoundError(username=self.username, course_id=self.course_id)


class LearnerListView(CourseViewMixin, generics.ListAPIView):
    """
    Get a paginated list of student data for a particular course.

    **Example Request**

        GET /api/v0/learners/?course_id={course_id}

    **Response Values**

        TODO

    **Parameters**

        You can specify the course ID for which you want data.

        TODO: add sorting/filtering

        course_id -- The course within which user data is requested.
        page -- The page of results which should be returned.
        page_size -- The maximum number of results which should be returned per page
        text_search -- A string to search over the name, username, and email of learners.
        segments -- A comma-separated string of segments to which
            learners should belong.  Semgents are "OR"-ed together.
            Can not use in combination with `ignore_segments`
            argument.
        ignore_segments -- A comma-separated string of segments to
            which learners should NOT belong.  Semgents are "OR"-ed
            together.  Can not use in combination with `segments`
            argument.
        cohort -- The cohort to which all returned learners must
            belong.
        enrollment_mode -- The enrollment mode to which all returned
            learners must belong.
        order_by -- The field for sorting the response.  Defaults to 'name'.
        sort_order -- The sort direction.  One of 'asc' or 'desc'.
            Defaults to 'asc'.

    """
    serializer_class = LearnerSerializer
    pagination_serializer_class = ElasticsearchDSLSearchSerializer
    paginate_by_param = 'page_size'
    paginate_by = learner.LEARNER_API_ROSTER_PAGE_SIZE
    max_paginate_by = 100  # TODO -- determine

    #
    # TODO: When should we return 404 if results list is empty?
    # e.g. what if user passes in a cohort which doesn't match anything?
    #

    def get(self, request, *args, **kwargs):
        # Cache the querystring arguments on the view object so that
        # we can access them in `self.get_queryset`.
        self.text_search = request.QUERY_PARAMS.get('text_search')
        self.segments = split_query_argument(request.QUERY_PARAMS.get('segments'))
        self.ignore_segments = split_query_argument(request.QUERY_PARAMS.get('ignore_segments'))
        self.cohort = request.QUERY_PARAMS.get('cohort')
        self.enrollment_mode = request.QUERY_PARAMS.get('enrollment_mode')
        self.order_by = request.QUERY_PARAMS.get('order_by')
        self.sort_order = request.QUERY_PARAMS.get('sort_order')
        return super(LearnerListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Fetches the user list from elasticsearch.  Note that an
        elasticsearch_dsl `Search` object is returned, not an actual
        queryset.
        """
        try:
            return RosterEntry.get_users_in_course(
                self.course_id,
                segments=self.segments,
                ignore_segments=self.ignore_segments,
                cohort=self.cohort,
                enrollment_mode=self.enrollment_mode,
                text_search=self.text_search,
                order_by=self.order_by,
                sort_order=self.sort_order
            )
        except ValueError as e:
            raise ParameterValueError(e.message)
