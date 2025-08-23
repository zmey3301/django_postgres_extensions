from django.contrib.gis.db.backends.postgis.operations import PostGISOperations

class DatabaseOperations(PostGISOperations):
    compiler_module = "django_postgres_extensions.models.sql.compiler"
