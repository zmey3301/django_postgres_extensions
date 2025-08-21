from django.contrib.gis.db.backends.postgis.operations import DatabaseOperations as BaseDatabaseOperations

class DatabaseOperations(BaseDatabaseOperations):
    compiler_module = "django_postgres_extensions.models.sql.compiler"
