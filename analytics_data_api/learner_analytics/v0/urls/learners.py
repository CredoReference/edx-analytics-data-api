from django.conf.urls import patterns, url

from analytics_data_api.learner_analytics.v0.views import learners as views

USERNAME_PATTERN = r'(?P<username>[^/+]+[/+][^/+]+[/+][^/]+)'
COURSE_URLS = [
    ('learners', views.LearnersListView, 'learners')
]

urlpatterns = []

for path, view, name in COURSE_URLS:
    regex = r'^{0}/{1}/$'.format(USERNAME_PATTERN, path)
    urlpatterns += patterns('', url(regex, view.as_view(), name=name))
