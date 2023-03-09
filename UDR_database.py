import numpy as np
import sqlite3 as sl
# Open the file in read mode
con = sl.connect('my-test.db')

with con:
    con.execute(""" 
        CREATE TABLE IF NOT EXISTS CLIENT ( 
            subscriber_No INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            tech INTEGER, 
            paid INTEGER 
        ); 
    """)
    sql = 'INSERT INTO CLIENT (subscriber_No, tech, paid) values(?, ?, ?)'
    data = [
    (1, 1, 21),
    (2, 1, 22),
    (3, 1, 23)
]
# with con:
    con.executemany(sql, data)
# with con:
    data = con.execute("SELECT * FROM CLIENT WHERE paid <= 22")
    for row in data:
        print(row)