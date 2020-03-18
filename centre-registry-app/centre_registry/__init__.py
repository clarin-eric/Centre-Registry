# from django.db.backends.signals import connection_created
#
#
# def deactivate_foreign_keys(sender, connection, **kwargs):
#     """Enable integrity constraint with sqlite."""
#     if connection.vendor == 'sqlite':
#         cursor = connection.cursor()
#         cursor.execute('PRAGMA foreign_keys = OFF;')
#
#
# connection_created.connect(deactivate_foreign_keys)