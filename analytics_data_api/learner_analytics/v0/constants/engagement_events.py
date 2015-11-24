from analytics_data_api.learner_analytics.v0.constants import engagement_entity_types

CREATED = 'created'
RESPONDED = 'responded'
COMMENTED = 'commented'

ATTEMPTED = 'attempted'
COMPLETED = 'completed'

PLAYED = 'played'

EVENTS = {
    engagement_entity_types.FORUM: [CREATED, RESPONDED, COMMENTED],
    engagement_entity_types.VIDEO: [ATTEMPTED, COMPLETED],
    engagement_entity_types.PROBLEM: [PLAYED],
}
