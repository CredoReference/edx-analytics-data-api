from django.conf import settings


class AnalyticsApiRouter(object):
    def db_for_read(self, model, **hints):  # pylint: disable=unused-argument
        return self._get_database(model)

    def _get_database(self, model):
        if model._meta.app_label in ['v0', 'learner_analytics_v0']:   # pylint: disable=protected-access
            return getattr(settings, 'ANALYTICS_DATABASE', 'default')

        return None

    def db_for_write(self, model, **hints):  # pylint: disable=unused-argument
        return self._get_database(model)

    def allow_relation(self, obj1, obj2, **hints):  # pylint: disable=unused-argument
        return self._get_database(obj1) == self._get_database(obj2)

    def allow_migrate(self, database, model):
        dest_db = self._get_database(model)
        if dest_db is not None:
            return database == dest_db
        else:
            return None
