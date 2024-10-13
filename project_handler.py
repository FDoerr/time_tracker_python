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


Database:                                 
+---------------------+           +-------------------+            
|      projects       |           |      sessions     |            
+---------------------+           +-------------------+            
| project_id (PK)     |<==+-------| session_id (PK)   |            
| project_name        |   |       | project_id (FK)   |            +------------------+
+---------------------+   |       | session_date      |            |      tasks       |
                          |       | time_spent        |            +------------------+
                          |       | task_id (FK)      |----------->| task_id (PK)     |
                          |       +-------------------+            | task_description |
                          +----------------------------------------| project_id (FK)  |
                                                                   +------------------+

'''

import sqlite3 as sql3
from typing import Any, Optional


def run_sql_command(db_path:str, cmd:str, data:Optional[tuple] = None) -> None:

    connection: sql3.Connection = sql3.connect(db_path)
    cursor: sql3.Cursor = connection.cursor()
    
    if data is None:
        cursor.execute(cmd)
    else:
        cursor.execute(cmd, data)

    connection.commit()
    cursor.close()
    connection.close()


#region create tables
def create_projects_table() -> None:

    cmd_create_projects_table:str = '''
                                    CREATE TABLE IF NOT EXISTS
                                    projects(
                                            project_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                            project_name    TEXT NOT NULL
                                            );
                                    '''
    
    run_sql_command('time_tracker_data.db', cmd_create_projects_table)


def create_sessions_table() -> None:

    cmd_create_sessions_table:str = '''
                                    CREATE TABLE IF NOT EXISTS
                                    sessions(
                                            session_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                            project_id      INTEGER NOT NULL,
                                            session_date    TEXT    NOT NULL,
                                            time_spent      INTEGER NOT NULL,
                                            task_id         INTEGER,
                                            FOREIGN KEY (project_id) REFERENCES projects (project_id)   ON DELETE CASCADE
                                            FOREIGN KEY (task_id)    REFERENCES tasks (task_id)         ON DELETE CASCADE
                                            );
                                    '''

    run_sql_command('time_tracker_data.db', cmd_create_sessions_table)


def create_tasks_table() -> None:
    cmd_create_tasks_table:str = '''
                                 CREATE TABLE IF NOT EXISTS
                                 tasks(
                                      task_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                                      project_id        INTEGER NOT NULL,
                                      task_description  TEXT,
                                      FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE
                                      );
                                 '''

    run_sql_command('time_tracker_data.db', cmd_create_tasks_table)
    
#endregion 


#region add to tables
def add_project(project_name:str) -> None:

    cmd_add_project:str = '''
                          INSERT INTO
                          projects(
                                  project_name
                                  ) 
                          VALUES(?);
                          '''
    
    run_sql_command('time_tracker_data.db', cmd_add_project, (project_name,))


def add_session(project_id:int, session_date:str, time_spent:int, task_id:int) -> None:

    cmd_add_session:str = '''
                          INSERT INTO
                          sessions(
                                  project_id,
                                  session_date,
                                  time_spent,
                                  task_id
                                  )
                          VALUES(?, ?, ?, ?);
                          '''    

    run_sql_command('time_tracker_data.db', cmd_add_session, (project_id, session_date, time_spent, task_id))


def add_task(project_id:int, task_description:str) -> None:

    cmd_add_task:str = '''
                       INSERT INTO
                       tasks(
                            project_id,
                            task_description
                            )
                       VALUES(?, ?);
                       '''

    run_sql_command('time_tracker_data.db', cmd_add_task, (project_id, task_description))

#endregion

#region query DB

def fetch_projects() -> list:

    cmd_get_projects:str ='SELECT * FROM projects'

    connection: sql3.Connection = sql3.connect('time_tracker_data.db')
    cursor: sql3.Cursor = connection.cursor()
    
    cursor.execute(cmd_get_projects)
    projects: list = cursor.fetchall()

    cursor.close()
    connection.close()
    return projects

#TODO: query session data for specific project

#TODO: query tasks for specific project



#endregion
if __name__== '__main__':
    projects = fetch_projects()
    for project in projects:
        print(project)