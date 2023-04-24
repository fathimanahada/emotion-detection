import sqlite3

# create a new database file
conn = sqlite3.connect('mydatabase.db')
# create a table for the data
# conn.execute('''
 #CREATE TABLE faces
# (
#     name TEXT PRIMARY KEY,
#     detection_time TEXT,
#      emotion TEXT
# )
# ''')
# open the data file
with open('emotion_labels.txt', 'r') as file:
    # read each line of the file
    for line in file:
        # split the line into fields
        fields = line.strip().split(',')
        # insert the data into the table
        # assume fields is a tuple with three values: name, detection_time, and emotion
        #fields = ('John', '2022-04-20', 'happy')

# execute the SQL statement with the fields
conn.execute('INSERT INTO emotions (name, detection_time, emotion) VALUES (?, ?, ?)', fields)

# commit the changes
conn.commit()

# close the database connection
conn.close()

