'''
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
                                                                   | task_done        |
                                                                   +------------------+

'''
#TODO: Refactor everything to use f-strings for better readability, this also means run_sql_command/query won't need the data tuples anymore
#TODO: modularize this Script
import sqlite3 as sql3

default_db:str = 'time_tracker_data.db'

#region sql execution functions

def run_sql_command(cmd:str,
                    data:tuple|None = None,
                    db_path:str     = default_db
                   ) -> None:

    connection:sql3.Connection|None = None
    cursor:sql3.Cursor|None         = None
    
    try:
        connection = sql3.connect(db_path)
        cursor = connection.cursor()    
    
        cursor.execute("PRAGMA foreign_keys = ON;") # enables foreign key restrictions

        if data is None:
            cursor.execute(cmd)
        else:
            cursor.execute(cmd, data)
        
        connection.commit()

    except sql3.OperationalError as operational_error:
        print(f'Operational Error occured: {operational_error}')
    except sql3.IntegrityError as integrity_error:
        print(f'Integrity Error occured: {integrity_error}')
    except Exception as error:
        print(f'Unexpected Error occured: {error}')

    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def run_sql_query(cmd:str,
                  data:tuple|None = None,
                  db_path:str     = default_db
                 ) -> list[dict]:
    
    connection:sql3.Connection|None = None
    cursor:sql3.Cursor|None         = None
    results = []
    
    try:
        connection = sql3.connect(db_path)
        connection.row_factory = sql3.Row # Set row factory to return rows as dictionaries
        cursor = connection.cursor()    

        cursor.execute("PRAGMA foreign_keys = ON;") # enables foreign key restrictions

        if data is None:
            cursor.execute(cmd)
        else:
            cursor.execute(cmd, data)

        results: list[dict] = [dict(row) for row in cursor.fetchall()]

    except Exception as error:
        print(f'Unexpected Error occured: {error}')

    finally:        
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    return results
#endregion


#region create tables
def create_projects_table() -> None:

    cmd_create_projects_table:str = '''
                                    CREATE TABLE IF NOT EXISTS
                                    projects(
                                            project_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                            project_name    TEXT NOT NULL
                                            );
                                    '''
    
    run_sql_command(cmd_create_projects_table)


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
                                            FOREIGN KEY (task_id)    REFERENCES tasks (task_id)
                                            );
                                    '''

    run_sql_command(cmd_create_sessions_table)


def create_tasks_table() -> None:

    cmd_create_tasks_table:str = '''
                                 CREATE TABLE IF NOT EXISTS
                                 tasks(
                                      task_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                                      project_id        INTEGER NOT NULL,
                                      task_description  TEXT,
                                      task_done         BOOLEAN NOT NULL DEFAULT 0 CHECK (task_done IN (0, 1)),
                                      FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE
                                      );
                                 '''

    run_sql_command(cmd_create_tasks_table)
    
#endregion

 
#region create triggers

def create_trigger_check_project_id_on_session_insert() -> None:

    cmd_create_trigger_check_project_id_on_session_insert:str = '''
                                                                CREATE TRIGGER IF NOT EXISTS
                                                                id_insert_trigger
                                                                BEFORE INSERT ON sessions
                                                                FOR EACH ROW
                                                                WHEN NEW.task_id IS NOT NULL
                                                                BEGIN
                                                                    SELECT CASE
                                                                        WHEN((SELECT project_id FROM tasks WHERE task_id = NEW.task_id) != NEW.project_id)
                                                                        THEN RAISE (ABORT, 'Task does not belong to the same project_id as the session.')
                                                                    END;
                                                                END;
                                                                '''
    
    run_sql_command(cmd_create_trigger_check_project_id_on_session_insert)


def create_trigger_check_project_id_on_session_update() -> None:

    cmd_create_trigger_check_project_id_on_session_update:str = '''
                                                                CREATE TRIGGER IF NOT EXISTS
                                                                id_update_trigger
                                                                BEFORE UPDATE ON sessions
                                                                FOR EACH ROW
                                                                WHEN NEW.task_id IS NOT NULL
                                                                BEGIN
                                                                    SELECT CASE
                                                                        WHEN((SELECT project_id FROM tasks WHERE task_id = NEW.task_id) != NEW.project_id)
                                                                        THEN RAISE (ABORT, 'Task does not belong to the same project_id as the session.')
                                                                    END;
                                                                END;
                                                                '''
    
    run_sql_command(cmd_create_trigger_check_project_id_on_session_update)

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
    
    run_sql_command(cmd_add_project, (project_name,))


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

    run_sql_command(cmd_add_session, (project_id, session_date, time_spent, task_id))


def add_task(project_id:int, task_description:str) -> None:

    cmd_add_task:str = '''
                       INSERT INTO
                       tasks(
                            project_id,
                            task_description                            
                            )
                       VALUES(?, ?);
                       '''

    run_sql_command(cmd_add_task, (project_id, task_description))

#endregion


#region query DB

def fetch_projects() -> list[dict]:

    cmd_get_projects:str ='SELECT * FROM projects;'

    projects: list[dict] = run_sql_query(cmd_get_projects)
    return projects


def fetch_sessions(project_id:int) -> list[dict]:

    cmd_get_session:str = '''
                          SELECT * FROM sessions
                          WHERE project_id = ?;
                          '''
    
    sessions: list[dict] = run_sql_query(cmd_get_session, (project_id,))
    return sessions


def fetch_tasks(project_id:int) -> list[dict]:

    cmd_get_tasks:str = '''
                        SELECT * FROM tasks
                        WHERE project_id = ?;
                        '''
    
    tasks: list[dict] = run_sql_query(cmd_get_tasks, (project_id,))
    return tasks


#endregion

#region delete entries

def del_project(project_id:int) -> None:
    
    cmd_del_project:str = '''
                          DELETE FROM projects 
                          WHERE project_id = ?;
                          '''
    
    run_sql_command(cmd_del_project, (project_id,))


def del_task(task_id:int) -> None:

    cmd_del_task:str = '''
                       DELETE FROM tasks 
                       WHERE task_id = ?;
                       '''
    
    run_sql_command(cmd_del_task, (task_id,))


def del_session(session_id:int) -> None:

    cmd_del_session:str = '''
                          DELETE FROM sessions 
                          WHERE session_id = ?;
                          '''
    
    run_sql_command(cmd_del_session, (session_id,))

#endregion



#region update entries

def update_project(new_project_name:str, project_id:int) -> None:

    cmd_update_project:str = '''
                             UPDATE projects
                             SET project_name = ?
                             WHERE project_id = ?;
                             '''
    
    run_sql_command(cmd_update_project, (new_project_name, project_id))


def update_session(session_id:      int,
                   new_project_id:  int|None = None,
                   new_session_date:str|None = None,
                   new_time_spent:  int|None = None,
                   new_task_id:     int|None = None) -> None:

    building_blocks_cmd:list[str] = []
    cmd_update_session = '''
                         UPDATE sessions
                         SET
                         '''
    
    if new_project_id is not None:
        building_blocks_cmd.append(f' project_id = {new_project_id}')        

    if new_session_date is not None:
        building_blocks_cmd.append(f' session_date = "{new_session_date}"')

    if new_time_spent is not None:
        building_blocks_cmd.append(f' time_spent = {new_time_spent}')

    if new_task_id is not None:
        building_blocks_cmd.append(f' task_id = {new_task_id}')
    

    if building_blocks_cmd == []:
       raise ValueError('At least one Optional field must be provided to update the session.')        

    cmd_update_session += ','.join(building_blocks_cmd)
    cmd_update_session += f' WHERE session_id = {session_id};'    
    
    run_sql_command(cmd_update_session)


def update_task(task_id:int,
                new_project_id:int|None = None,
                new_task_description:str|None = None,
                new_task_done:bool|None = None
                ) -> None:
    
    building_blocks_cmd:list[str] = []

    cmd_update_task = '''
                      UPDATE tasks
                      SET
                      '''
    
    if new_project_id is not None:
        building_blocks_cmd.append(f' project_id = {new_project_id}')        

    if new_task_description is not None:
        building_blocks_cmd.append(f' task_description = "{new_task_description}"')

    if new_task_done is not None:        
        building_blocks_cmd.append(f' task_done = {new_task_done}')
    
    if building_blocks_cmd == []:
       raise ValueError('At least one Optional field must be provided to update the task.')
        
    cmd_update_task += ','.join(building_blocks_cmd)
    cmd_update_task += f' WHERE task_id = {task_id};'    
    
    run_sql_command(cmd_update_task)

    
def update_task_description(task_id:int, new_task_description:str) -> None:
    #simplified version of update tasks which might be more usefull
    cmd_update_task_description = '''
                                  UPDATE tasks
                                  SET task_description = ?
                                  WHERE task_id = ?;
                                  '''
    
    run_sql_command(cmd_update_task_description, (new_task_description, task_id))

#endregion


#region if __name__=='__main__':
if __name__=='__main__':
    print(f'Runs directly: {__file__}!')
    # print(fetch_projects())
    # print(fetch_sessions(1))
    # print(fetch_tasks(1))
    # update_project('Project_name changed', 1)
    # update_task(1, 1)
    # update_session(2, 2, 'new date', 666, 1)
    # update_session(1, new_task_id=5)  
    # update_task(3, new_project_id = 2)
    # update_task(1, 2, 'test')    
    # update_task(2, new_task_description='test')   
    # update_task(1) 
    # #del_project(1)
    # #del_session(1)
    # create_projects_table()
    # create_sessions_table()
    # create_tasks_table()
    # create_trigger_check_project_id_on_session_insert()
    # create_trigger_check_project_id_on_session_update()
    # add_project('Projekt 1')
    # add_project('Projekt 2')
    # add_project('Projekt 3')
    # add_task(1, 'Task 1')
    # add_task(1, 'Task 2')
    # add_task(2, 'Task 3')
    # add_task(2, 'Task 4')
    # add_task(3, 'Task 5')
    # #add_task(4, 'Task 6') ging nicht weil project 4 nicht exisitert 
    # add_session(1, str(datetime.now()), 1000, None)
    # add_session(1, str(datetime.now()), 2000, 1)
    # add_session(1, str(datetime.now()), 3000, 3) # geht nicht mehr weil sessions.project_id = 1 und tasks.project_id = 2
    # add_session(2, str(datetime.now()), 4000, 3)
    # #add_session(1, str(datetime.now()), 5000, 10) # ging nicht weil taks_id = 10 nicht exisitert
    # #add_session(10, str(datetime.now()), 5000, 1) # ging nicht weil project_id = 10 nicht existiert