# Convert file existing_db.db to SQL dump file dump.sql
from sqlite3 import connect

con = connect('Centre_Registry.sqlite')
with open('dump.sql', 'w') as f:
    for line in con.iterdump():
        f.write('%s\n' % line)