from django.conf.urls import patterns, url

from analytics_data_api.v0.views import learners as views


USERNAME_PATTERN = r'(?P<username>.+)'

urlpatterns = patterns(
    '',
    url(r'^learners/', views.LearnerListView.as_view(), name='learners'),
    url(r'^learners/{}'.format(USERNAME_PATTERN), views.LearnerView.as_view(), name='learner'),
)
