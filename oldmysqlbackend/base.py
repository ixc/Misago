from django.db.backends.mysql.base import *
from .schema import MisagoMySqlDatabaseSchemaEditor

DatabaseWrapper.SchemaEditorClass = MisagoMySqlDatabaseSchemaEditor
