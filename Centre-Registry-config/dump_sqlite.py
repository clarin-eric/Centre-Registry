# Convert file existing_db.db to SQL dump file dump.sql
from sqlite3 import connect

with open('dump.sql', 'w') as f:
    for line in connect('Centre_Registry.sqlite').iterdump():
        f.write('%s\n' % line)
