from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^learners/', include('analytics_data_api.learner_analytics.v0.urls.learners', namespace='learners')),
)
