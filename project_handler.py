'''
project_handler:

list Projects in combobox
create new Projects via combobox
store those projects in a file
retrieve those projects on startup


save time to currently active Project via Save button


focusin -> load list from file
return  -> save new item to file


data i need:
Project Name
    session date + current time
        time in session
        topic

    session date + current time
        time in session
        topic
    
    session date + current time
        time in session
        topic
    ...

Project Name
    session date + current time
        time in session
        topic

    session date + current time
        time in session
        topic
    
    session date + current time
        time in session
        topic
    ...
    
   

'''
session_data: dict  = {'Session Date' : 'Datum und Uhrzeit',
                        'Session time': 10000,
                        'topic' : 'Todo-List point'}
project_dict: dict  = {'project_name' : 'Projekt 1', 'session_data' : session_data}
projects_dict: dict = {'projects' : project_dict}

print(projects_dict)
