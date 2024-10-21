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
from datetime import datetime

# def run_sql_command(db_path:str, cmd:str, data:Optional[tuple] = None) -> None:
#     #TODO: add try except finally
#     connection: sql3.Connection = sql3.connect(db_path)
#     cursor: sql3.Cursor = connection.cursor()

#     cursor.execute("PRAGMA foreign_keys = ON;") # enables foreign key restrictions


#     if data is None:
#         cursor.execute(cmd)
#     else:
#         cursor.execute(cmd, data)

#     connection.commit()
#     cursor.close()
#     connection.close()
def run_sql_command(db_path:str, cmd:str, data:Optional[tuple] = None) -> None:

    connection = None
    cursor = None
    
    try:
        connection: sql3.Connection = sql3.connect(db_path)
        cursor: sql3.Cursor = connection.cursor()
    
        cursor.execute("PRAGMA foreign_keys = ON;") # enables foreign key restrictions

        if data is None:
            cursor.execute(cmd)
        else:
            cursor.execute(cmd, data)

    except sql3.IntegrityError as integrity_error:
        print(f'Integrity Error occured: {integrity_error}')

    finally:
        connection.commit()
        cursor.close()
        connection.close()

def create_trigger_check_project_id_on_session_insert() -> None:

    cmd_create_trigger_check_project_id_on_session_insert:str = '''
                                                                CREATE TRIGGER IF NOT EXISTS
                                                                id_trigger
                                                                BEFORE INSERT ON sessions
                                                                FOR EACH ROW
                                                                WHEN NEW.task_id IS NOT NULL
                                                                BEGIN
                                                                    SELECT CASE
                                                                        WHEN((SELECT project_id FROM tasks WHERE task_id = NEW.task_id) != NEW.project_id)
                                                                        THEN RAISE (ABORT, 'task does not belong to the same project_id as the session.')
                                                                    END;
                                                                END;
                                                                '''
    
    run_sql_command('time_tracker_data.db', cmd_create_trigger_check_project_id_on_session_insert)

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

def run_sql_query(db_path:str, cmd:str, data:Optional[tuple] = None)  -> list[dict]:
    #TODO: add try except finally
    connection: sql3.Connection = sql3.connect(db_path)
    connection.row_factory = sql3.Row
    cursor: sql3.Cursor = connection.cursor()    

    cursor.execute("PRAGMA foreign_keys = ON;") # enables foreign key restrictions

    if data is None:
        cursor.execute(cmd)
    else:
        cursor.execute(cmd, data)

    results: list[dict] = [dict(row) for row in cursor.fetchall()]

    cursor.close()
    connection.close()
    return results


def fetch_projects() -> list[dict]:

    cmd_get_projects:str ='SELECT * FROM projects;'

    projects: list[dict] = run_sql_query('time_tracker_data.db', cmd_get_projects)
    return projects


def fetch_sessions(project_id:int) -> list[dict]:

    cmd_get_session:str = '''
                          SELECT * FROM sessions
                          WHERE project_id = ?;
                          '''
    
    sessions: list[dict] = run_sql_query('time_tracker_data.db', cmd_get_session, (project_id,))
    return sessions


def fetch_tasks(project_id:int) -> list[dict]:

    cmd_get_tasks:str = '''
                        SELECT * FROM tasks
                        WHERE project_id = ?;
                        '''
    
    tasks: list[dict] = run_sql_query('time_tracker_data.db', cmd_get_tasks, (project_id,))
    return tasks


#endregion

#region delete entries
#TODO
def del_project(project_id) -> None:
    
    cmd_del_project:str = '''
                          DELETE FROM projects 
                          WHERE project_id=?
                          '''
    
    run_sql_command('time_tracker_data.db', cmd_del_project, (project_id,))

def del_task(task_id) -> None:

    cmd_del_task:str = '''
                          DELETE FROM tasks 
                          WHERE task_id=?
                          '''
    
    run_sql_command('time_tracker_data.db', cmd_del_task, (task_id,))


def del_session(session_id) -> None:

    cmd_del_session:str = '''
                          DELETE FROM sessions 
                          WHERE session_id=?
                          '''
    
    run_sql_command('time_tracker_data.db', cmd_del_session, (session_id,))

#endregion



#region change entries
#TODO

#endregion
if __name__=='__main__':
    #del_project(1)
    #del_session(1)
    create_projects_table()
    create_sessions_table()
    create_tasks_table()
    create_trigger_check_project_id_on_session_insert()
    add_project('Projekt 1')
    add_project('Projekt 2')
    add_project('Projekt 3')
    add_task(1, 'Task 1')
    add_task(1, 'Task 2')
    add_task(2, 'Task 3')
    add_task(2, 'Task 4')
    add_task(3, 'Task 5')
    #add_task(4, 'Task 6') ging nicht weil project 4 nicht exisitert 
    add_session(1, str(datetime.now()), 1000, None)
    add_session(1, str(datetime.now()), 2000, 1)
    add_session(1, str(datetime.now()), 3000, 3) # geht nicht mehr weil sessions.project_id = 1 und tasks.project_id = 2
    add_session(2, str(datetime.now()), 4000, 3)
    #add_session(1, str(datetime.now()), 5000, 10) # ging nicht weil taks_id = 10 nicht exisitert
    #add_session(10, str(datetime.now()), 5000, 1) # ging nicht weil project_id = 10 nicht existiert