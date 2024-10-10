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
      project_id (PK)
      project_name

sessions:
      session_id(PK)
      project_id(FK)
      time_spent
      date
      task

      
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
| project_id (PK)     |<----------| session_id (PK)   |            
| project_name        |           | project_id (FK)   |            +-------------------+
+---------------------+           | session_date      |            |      task         |
                                  | time_spent        |            +-------------------+
                                  | task_id (FK)      |----------->|  task_id (PK)     |
                                  +-------------------+            |  task_description |
                                                                   +-------------------+

'''

import sqlite3