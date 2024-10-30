import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import sv_ttk #https://github.com/rdbende/Sun-Valley-ttk-theme

from timer import Timer
import project_handler as db
#TODO: change to this style: https://ttkbootstrap.readthedocs.io/en/version-0.5/tutorial.html
#TODO: editable Treeview cells: https://www.youtube.com/watch?v=n5gItcGgIkk
#TODO: total time spent label functionality
#TODO: Functionality to add:
#     [X] add Project
#     [X]     -> Populate projects dropdown
#     [ ]         -> add task
#     [ ]             -> populate tasks
#     [ ]                 -> save session | add to log
#     [ ]                     -> populate logs
#     [ ]                         -> delete project/task/session


# global variables
timer_button_default_text: str = '⏺ start timer '
timer_display_delay_in_ms:int = 50
# initialization
timer:Timer =Timer() 


#region Stopwatch button related functions
def reset() -> None:
    timer.stop()
    timer.reset()
    session_time_button.config(text=timer_button_default_text)
    
    
def press_timer_button() -> None:
    if timer.running:
        timer.stop()
    else:
        timer.start()
        update_timer_display()

def update_timer_display() -> None:
        
        if timer.was_reset: #prevents timer_display from updating to 00:00:00 when reset while running
            return
        
        elapsed_time: int = timer.get_elapsed_time()        
        hours, minutes, seconds = calculate_hours_minutes_seconds(elapsed_time)
        formated_time:str = f"{hours:02}:{minutes:02}:{seconds:02}"

        if timer.running:
            session_time_button.config(text=f"⏸ {formated_time}") # ⏵⏸ ⏯ ⏺
            root.after(timer_display_delay_in_ms, update_timer_display) #call function after 100ms, keeps UI Responsive
        else:
           session_time_button.config(text=f"⏵ {formated_time}") 
      

def calculate_hours_minutes_seconds(elapsed_time_in_s:int) -> tuple[int, int, int]:
    hours   = int( elapsed_time_in_s / 3600)  
    minutes = int((elapsed_time_in_s % 3600) / 60)  
    seconds = int(elapsed_time_in_s  % 60)
    return hours, minutes, seconds
 #endregion


#region project related functions

def add_project() -> None: 
    project_name: str | None = simpledialog.askstring('New Project', 'Enter new project name: ')
    if project_name is not None:
        db.add_project(project_name)
    
#TODO
def del_project():
    print('Delete Project Button pressed')
    ...

def select_project(event):
    print('Project selected')
    update_task_display()
    update_session_log_display()
    ...

def fetch_projects() -> list[dict]:    
    projects: list[dict] = db.fetch_projects()    
    return projects
    

def update_projects_display(projects:list[dict]) -> None:
    project_list: list[str]= []
    for project in projects:
        project_str: str = f'{project['project_id']} | {project['project_name']}'
        project_list.append(project_str)
    
    project_title_combobox['values'] = project_list
    

def click_projects_combobox() -> None:    
    projects: list[dict] = fetch_projects()
    update_projects_display(projects)

#endregion

#region task list related functions
#TODO
def add_task():
    print('add task button pressed')
    ...

def del_task():
    print('delete task button pressed')
    ...

def fetch_tasks():
    print('fetching tasks')
    ...

def update_task_display():
    print('updating tasks display')
    fetch_tasks()    
    
    for i in range(1, 10):
        task_list_tree.insert('','end', values=[i])
    ...
#endregion

#region session log related functions
#TODO
def add_session():
    print('save button pressed | add session')
    ...

def del_session():
    print('delete session button pressed')
    ...

def fetch_session_logs():
    print('fetching session_logs')
    ...

def update_session_log_display():
    print('updating session_log_display')
    fetch_session_logs()
    for i in range(1, 10):
        log_tree.insert('','end', values=(i, i, i))
    
    ...
#endregion

#region GUI setup
#window setup
root = tk.Tk()
sv_ttk.use_dark_theme()
root.title('time_tracker')
root.geometry('675x475') #width x height
root.minsize(width=400, height=300)


#region project UI Elements
#project display frame
project_display_frame = ttk.Frame(root)
project_display_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.NW)
# project_title_combobox
project_name = tk.StringVar(value= 'Project name')
project_title_combobox = ttk.Combobox(project_display_frame, textvariable = project_name, state='readonly',height=5, postcommand=click_projects_combobox)
project_title_combobox.bind('<<ComboboxSelected>>', select_project)
project_title_combobox.pack(side=tk.LEFT, padx=10)
# add project button
add_project_button = ttk.Button(project_display_frame, text='Add Project', command=add_project)
add_project_button.pack(side=tk.LEFT, padx=10)
# delete project button
delete_project_button = ttk.Button(project_display_frame, text='delete Project', command=del_project)
delete_project_button.pack(side=tk.LEFT, padx=10)
#endregion

#region total time label UI Elements
# subframe to group total time labels
frame_total_time =ttk.Frame(root)
frame_total_time.grid(row=2, column=1, padx = 50, pady = 10, sticky=tk.EW)
# total_time_label_name
total_time_label_name = ttk.Label(frame_total_time, text = 'Total: ')
total_time_label_name.pack(padx = 10, pady = 10)

# total_time_label
total_time = tk.StringVar(value= 'dd:hh:mm:ss')
total_time_label = ttk.Label(frame_total_time, textvariable = total_time)
total_time_label.pack(padx = 10, pady = 10)
#endregion



#region todo list UI Elements
# frame for treeview & scrollbar
task_frame = ttk.Frame(root)
task_frame.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
# task tree frame
task_tree_frame = ttk.Frame(task_frame)
task_tree_frame.pack(side=tk.TOP, padx=10, pady=5)
# treeview
task_list_tree_columns = ('ToDo: ',)
task_list_tree = ttk.Treeview(task_tree_frame,
                              columns    = task_list_tree_columns,
                              show       = "headings",
                              selectmode = "browse",
                              height     = 3)
task_list_tree.heading(column='ToDo: ', text='ToDo: ')
# scrollbar
task_list_scrollbar = ttk.Scrollbar(task_tree_frame, orient=tk.VERTICAL, command=task_list_tree.yview)
task_list_tree.configure(yscrollcommand=task_list_scrollbar.set)
# Place  treeview and scrollbar
task_list_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
task_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# task button frame
task_button_frame = ttk.Frame(task_frame)
task_button_frame.pack(side=tk.BOTTOM, padx=0, pady=5)
# add task button
add_task_button = ttk.Button(task_button_frame, text='Add Task', command=add_task)
add_task_button.pack(side=tk.LEFT, padx=5, pady=5)
# delete task button
delete_task_button = ttk.Button(task_button_frame, text='Delete Task', command=del_task)
delete_task_button.pack(side=tk.RIGHT, padx=5, pady=5)
#endregion


#region session log UI Elements
# frame for treeview & scrollbar
log_frame = ttk.Labelframe(root, text='logs')
log_frame.grid(row=6, column=1, padx=10, pady=10)
# log tree & scrollbar frame
log_tree_frame = ttk.Frame(log_frame)
log_tree_frame.pack(side=tk.TOP, padx=5, pady=5)
# treeview
log_tree_column=  ('Date', 'Duration', 'Task')
log_tree = ttk.Treeview(log_tree_frame,
                        columns     = log_tree_column,
                        show        = "headings",
                        selectmode  = tk.BROWSE,
                        height      = 4)
log_tree.heading(column=log_tree_column[0], text=log_tree_column[0])
log_tree.heading(column=log_tree_column[1], text=log_tree_column[1])
log_tree.heading(column=log_tree_column[2], text=log_tree_column[2])
# scrollbar
log_scrollbar = ttk.Scrollbar(log_tree_frame, orient=tk.VERTICAL, command=log_tree.yview)
log_tree.configure(yscrollcommand=log_scrollbar.set)
# Place  treeview and scrollbar
log_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#delete session button
delete_session_button = ttk.Button(log_frame, text = 'Delete Session', command= del_session)
delete_session_button.pack(side=tk.BOTTOM, padx=5, pady=5)
#endregion

#region Timer Button UI Elements
# reset & save frame
frame_reset_save = ttk.Frame(root)
frame_reset_save.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E)
# session_time_button
session_time_button = ttk.Button(frame_reset_save, text = timer_button_default_text , command = press_timer_button)
session_time_button.pack(side=tk.LEFT, padx = 10, pady = 10, fill=tk.BOTH)
# reset_button
reset_button = ttk.Button(frame_reset_save, text = 'Reset', command = reset)
reset_button.pack(side=tk.BOTTOM, padx = 10, pady = 10)
# save_button
save_button = ttk.Button(frame_reset_save, text = 'Save', command=add_session)
save_button.pack(side=tk.TOP, padx = 10, pady = 10)
#endregion

#endregion