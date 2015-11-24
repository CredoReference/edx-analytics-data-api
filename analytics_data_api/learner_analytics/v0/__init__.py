from django.apps import AppConfig


class LearnerAnalyticsConfig(AppConfig):
    """
    Because we have two v0 apps, we would get get naming conflicts without explicitly
    setting the label.
    """
    name = 'analytics_data_api.learner_analytics.v0'
    label = 'learner_analytics_v0'
