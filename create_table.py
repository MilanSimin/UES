import sqlite3 as lite
import sys

con = lite.connect('sensorsdata.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS HCSR04_data")
    cur.execute("CREATE TABLE HCSR04_data(timestamp DATETIME, dist NUMERIC)")
