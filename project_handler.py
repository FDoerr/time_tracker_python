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
[name, Date, time, topic]

{'projects': 
        [{ 'project_name': 'Projekt 1',
            'session_data': [
                            {'Session Date': 'Datum und Uhrzeit', 'Session time': 10000, 'topic': 'Todo-List point'}
                            {'Session Date': 'Datum und Uhrzeit', 'Session time': 10000, 'topic': 'Todo-List point'}
                            ]
        },
        { 'project_name': 'Projekt 1',
            'session_data': [
                            {'Session Date': 'Datum und Uhrzeit', 'Session time': 10000, 'topic': 'Todo-List point'}
                            {'Session Date': 'Datum und Uhrzeit', 'Session time': 10000, 'topic': 'Todo-List point'}
                            ]
        }
        }]
}

{'projects': 
        {
        'project_id': 'Projekt 1',
        'session_data':
                    {'Session Date': 'Datum und Uhrzeit', 'Session time': 10000, 'topic': 'Todo-List point'}
        }
}


'''
session_data1: dict  = {'Session Date' : '1 Datum und Uhrzeit',
                        'Session time': 10000,
                        'topic' : '1 Todo-List point'}
session_data2: dict  = {'Session Date' : '2 Datum und Uhrzeit',
                        'Session time': 20000,
                        'topic' : '2 Todo-List point'}
project_dict1: dict  = {'project_name' : 'Projekt 1', 'session_data' : [session_data1, session_data2]}
project_dict2: dict  = {'project_name' : 'Projekt 1', 'session_data' : [session_data1, session_data2]}
projects_dict: dict  = {'projects' : [project_dict1, project_dict2]}

print(projects_dict)

dictionary:dict  = {
    "projects": [
      {
        "project_name": "Projekt 1",
        "session_data": [
          {
            "Session Date": "1 Datum und Uhrzeit",
            "Session time": 10000,
            "topic": "1 Todo-List point"
          },
          {
            "Session Date": "2 Datum und Uhrzeit",
            "Session time": 20000,
            "topic": "2 Todo-List point"
          }
        ]
      },
      {
        "project_name": "Projekt 1",
        "session_data": [
          {
            "Session Date": "1 Datum und Uhrzeit",
            "Session time": 10000,
            "topic": "1 Todo-List point"
          },
          {
            "Session Date": "2 Datum und Uhrzeit",
            "Session time": 20000,
            "topic": "2 Todo-List point"
          }
        ]
      }
    ]
  }

if dictionary == projects_dict:
    print(True)