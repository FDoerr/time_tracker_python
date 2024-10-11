'''

project_handler:
list Projects in combobox
create new Projects via combobox
store those projects in a file/database
retrieve those projects on startup
build database if nonexistent

Combobox:
focusin -> load list from databse
return  -> save new item to database
Button:
save time to currently active Project via Save button


data i need: [name, Date, time, task]
Project Name
    session date + current time
        time in session
        task

    session date + current time
        time in session
        task
    
    session date + current time
        time in session
        task
    ...

Project Name
    session date + current time
        time in session
        task
    ...

        

with a sql Database:
Database: Projekte:_Tracker
        Table: Projekt 1
        Table: Projekt 2
        ...
            Daten: [Date, time, task]
            ...

projects:
      project_id (PK)   INTEGER
      project_name      TEXT

sessions:
      session_id(PK)    INTEGER
      project_id(FK)    INTEGER
      time_spent        INTEGER
      date              TEXT
      task              TEXT

      
+---------------------+           +-------------------+
|      projects       |           |      sessions     |
+---------------------+           +-------------------+
| project_id (PK)     |<----------| session_id (PK)   | 
| project_name        |           | project_id (FK)   |
+---------------------+           | session_date      |
                                  | time_spent        |
                                  | task              |
                                  +-------------------+

+---------------------+           +-------------------+            
|      projects       |           |      sessions     |            
+---------------------+           +-------------------+            
| project_id (PK)     |<==+-------| session_id (PK)   |            
| project_name        |   |       | project_id (FK)   |            +------------------+
+---------------------+   |       | session_date      |            |      task        |
                          |       | time_spent        |            +------------------+
                          |       | task_id (FK)      |----------->| task_id (PK)     |
                          |       +-------------------+            | task_description |
                          +----------------------------------------| project_id (FK)  |
                                                                   +------------------+

'''

import sqlite3 as sql3
from datetime import datetime
from typing import Literal

connection: sql3.Connection = sql3.connect('time_tracker_data.db')
cursor: sql3.Cursor = connection.cursor()

cmd_projects_create:str = '''CREATE TABLE IF NOT EXISTS
                              projects(
                              project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              project_name TEXT NOT NULL
                              );
                          '''

cmd_sessions_create:str = '''CREATE TABLE IF NOT EXISTS
                              sessions(
                              session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              project_id INTEGER NOT NULL,
                              session_date TEXT NOT NULL,
                              time_spent INTEGER NOT NULL,
                              task TEXT,
                              FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE
                              );
                          '''

cmd_add_project:str = '''INSERT INTO projects
                          (project_name)
                          VALUES(?)
                          ;''' #,(project_name,)

cmd_add_session:str = '''INSERT INTO sessions
                          ()
                          VALUES(?, ?, ?, ?)
                          ;''' #,(project_id, session_date, time_spent, task)


cursor.execute(cmd_projects_create)
cursor.execute(cmd_sessions_create)
cursor.execute(cmd_add_project, ('Projekt 1',)) # ('Projekt 1',) isn't treated as a tuple without a comma
cursor.execute(cmd_add_project, ('Projekt 2',))
cursor.execute(cmd_add_project, ('Projekt 3',))
cursor.execute(cmd_add_session, (int(1), str(datetime.now()), int(10000), str('Task 1')))
connection.commit()
cursor.close()
connection.close()