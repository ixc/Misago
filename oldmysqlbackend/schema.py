from django.db.backends.mysql.schema import *


class MisagoMySqlDatabaseSchemaEditor(DatabaseSchemaEditor):

    sql_create_table = "CREATE TABLE %(table)s (%(definition)s) ROW_FORMAT = DYNAMIC"
