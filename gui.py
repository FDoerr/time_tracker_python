import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime

from  ttkbootstrap import Style #https://ttkbootstrap.readthedocs.io

from timer import Timer
import project_handler as db


#TODO: deal with long task descriptions and project names
#TODO: Functionality to add:
#     [X] add Project
#     [X]     -> Populate projects dropdown
#     [X]         -> add task
#     [X]             -> populate tasks
#     [X]                 -> save session | add to log
#     [X]                     -> populate logs
#     [X]                         -> delete project/session
#     [X]                               -> make logs more readable (task_id and time_spent)
#     [X]                                   -> mark tasks as done
#     [ ]                                       -> change del task to tag as deleted but don't delete

# global variables
timer_button_default_text: str = '⏺ start timer '
timer_display_delay_in_ms: int = 50


# initialization
timer:Timer =Timer() 


#region general functions

def calculate_hours_minutes_seconds(elapsed_time_in_s:int) -> tuple[int, int, int]:
    hours:   int = int( elapsed_time_in_s / 3600)  
    minutes: int = int((elapsed_time_in_s % 3600) / 60)  
    seconds: int = int(elapsed_time_in_s  % 60)
    return hours, minutes, seconds


def get_id_from_treeview(treeview: ttk.Treeview) -> int | None:
    '''
    returns None if not item is selected
    returns last item in values of treeview dict
    this assumes the last value is the id
    '''

    selected_item:str = treeview.focus()
    if selected_item == '': # no item selected
        return None

    selected_item_dict: dict = treeview.item(selected_item)
    values_list: list        = selected_item_dict['values']    
    id: int                  = values_list[-1]    
    if type(id) is not int:
        raise TypeError(f'Last Value {id=} in {treeview=} not of expected type.')
        
    return id

#endregion

#region Stopwatch button related functions

def reset() -> None:
    timer.stop()
    timer.reset()
    update_total_time_display()
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
    hours, minutes, seconds  = calculate_hours_minutes_seconds(elapsed_time)
    formated_time:str = f"{hours:02}:{minutes:02}:{seconds:02}"

    # toggle displayed symbol ⏺ ⏵⏸ ⏯ 
    if timer.running:
        session_time_button.config(text=f"⏸ {formated_time}")
        root.after(timer_display_delay_in_ms, update_timer_display) #call function after 100ms, keeps UI Responsive
    else:
       session_time_button.config(text=f"⏵ {formated_time}") 
    
    update_total_time_display()


def update_total_time_display() -> None:

    elapsed_time: int = timer.get_elapsed_time()
    for item in log_tree.get_children():
        elapsed_time += int(log_tree.item(item)['values'][-3])

    hours, minutes, seconds  = calculate_hours_minutes_seconds(elapsed_time)
    formated_time:str = f"{hours:02}:{minutes:02}:{seconds:02}"    

    total_time.set(formated_time)  


 #endregion


#region project related functions
def add_project() -> None: 
    project_name: str | None = simpledialog.askstring('New Project', 'Enter new project name: ')
    if project_name in project_title_combobox.project_dict:
        messagebox.showwarning("Duplicate Entry", "This project name already exists.")
        return
    elif project_name == '':
        messagebox.showinfo('No Project Name', 'Enter project name.')
        return
    elif project_name is None: # if cancel button was pressed
        return
    else:
        db.add_project(project_name)
        select_last_project_in_dropdown()
        update_task_and_session_display()


def del_project() -> None:
    selected_project_id: int = get_selected_project()
    if selected_project_id is None:
        messagebox.showwarning('No Active Project', 'Please select project')
        return
    
    confirmation: bool = messagebox.askyesno('Delete Project', 'Do you really want to delete the project?\nThis will also deletes all associated session logs and tasks')
    if confirmation == True: 
        db.del_project(selected_project_id)
        select_last_project_in_dropdown()
        update_task_and_session_display()
    else:
        return 
    

def fetch_projects() -> list[dict]:    
    projects: list[dict] = db.fetch_projects()    
    return projects


def click_projects_combobox() -> None:    
    projects: list[dict] = fetch_projects()
    update_projects_display(projects)


def update_projects_display(projects:list[dict]) -> None:
    new_project_dict = dict()
    for project in projects:
        new_project_dict[project['project_name']] = project['project_id'] # using the name as a key, is easier for finding ID
    
    project_title_combobox['values']    = list(new_project_dict.keys())
    project_title_combobox.project_dict = new_project_dict # "reverse" dict for referencing id from name


def select_last_project_in_dropdown() -> None:
    click_projects_combobox() # to refresh combobox values
    projects = project_title_combobox['values']   
    
    if projects != '': # prevent index error when only one project exists and gets deleted
        project_title_combobox.set(projects[-1])


def update_task_and_session_display() -> None:      
    selected_project_id: int =  get_selected_project()
    tasks: list[dict] = fetch_tasks(selected_project_id)
    update_task_display(tasks)
    session_logs: list[dict] = fetch_session_logs(selected_project_id)
    update_session_log_display(session_logs)  
    update_total_time_display()


def click_update_task_and_session_display(event) -> None: # handles the event
    update_task_and_session_display()


def get_selected_project() -> int:
    selected_project_id: int =  project_title_combobox.project_dict.get(project_title_combobox.get())
    return selected_project_id 

#endregion

#region task list related functions
def add_task() -> None:
    selected_project_id: int = get_selected_project()     
    if selected_project_id is None:
        messagebox.showwarning('No Active Project', 'Please select project')
        return
    
    task_name: str | None = simpledialog.askstring('New Task', 'Enter new Task Descriptor: ') 
    if task_name == '':
        messagebox.showinfo('No Task Descriptior', 'Enter task descriptor.')
        return
    elif task_name is None: # if cancel button was pressed
        return
    else:
        db.add_task(selected_project_id, task_name)
        update_task_and_session_display()

        
#TODO: this works but throws sql Integrity Error Foreign Key constraint failed, when deleting task that is also in session log
#           ->  mark tasks as deleted in DB and only show non deleted ones?
#           -> delete them with trigger if no session log references them anymore?
def del_task() -> None:
    try:
        task_id: int | None =  get_id_from_treeview(task_list_tree)
        if task_id is None: 
            messagebox.showwarning('No Task Selected', 'Please select task')
            return
        db.del_task(task_id)
        update_task_and_session_display()    
        
    except TypeError as e:
        messagebox.showerror('Last Value not of expected type', f'{e}')
    except Exception as e:
        messagebox.showerror('Unexpected exception', f'Unexpected exception {e}')
        

def toggle_task_done() -> None:    
    try:
        task_id: int|None   =  get_id_from_treeview(task_list_tree) 
        task_done: bool|None = get_task_done_from_treeview(task_list_tree)

        if task_id is None or task_done is None:
            messagebox.showwarning('No Task Selected', 'Please select task')
            return
                
        db.update_task(task_id, new_task_done = not task_done)
        update_task_and_session_display()  

    except TypeError as e:
        messagebox.showerror('Last Value not of expected type', f'{e}')
    except Exception as e:
        messagebox.showerror('Unexpected exception', f'Unexpected exception {e}')
            

def get_task_done_from_treeview(treeview) -> None | bool:
    selected_item:str = treeview.focus()
    if selected_item == '': # no item selected
        return None

    selected_item_dict: dict = treeview.item(selected_item)
    values_list: list        = selected_item_dict['values']    
    task_done: int           = values_list[-2]  

    if task_done not in (0, 1):
        raise TypeError(f'Last Value {id=} in {treeview=} not of expected type.')
        
    return bool(task_done)

def fetch_tasks(selected_project_id) -> list[dict]:    
    tasks: list[dict] = db.fetch_tasks(selected_project_id)    
    return tasks    


def update_task_display(tasks:list[dict]) -> None:        
    for item in task_list_tree.get_children():
        task_list_tree.delete(item)

    #task_list_tree_columns: tuple = ('Done: ', 'ToDo: ', 'task_done', 'task_id')
    for task in tasks:          
        if task['task_done'] == 1:
            done_str:str = '✓'  
        else:
            done_str = '' 

        task_list_tree.insert('', task['task_id'], values=(done_str,
                                                           task['task_description'],
                                                           task['task_done'],
                                                           task['task_id']))

    
#endregion

#region session log related functions

def add_session() -> None:
    if timer.running: 
        press_timer_button() # pause timer    

    project_id: int = get_selected_project()
    if project_id is None:
        messagebox.showinfo('No Active Project', 'Please select project')
        return    
    
    date: str       = datetime.now().strftime('%d.%m.%y %H:%M:%S')        
    time_spent: int = timer.get_elapsed_time()

    task_id: int | None = None    
    try:
        task_id = get_id_from_treeview(task_list_tree) 
    except TypeError as e:
        messagebox.showerror('Last Value not of expected type', f'{e}')
        return
    except Exception as e:
        messagebox.showerror('Unexpected exception', f'Unexpected exception {e}')
        return    
    if task_id == None:
            messagebox.showwarning('No Task Selected', 'Please select task')
            return  
            
    db.add_session(project_id, date, time_spent, task_id)
    update_task_and_session_display() 
    

def del_session() -> None:
    try:
        session_log_id: int | None =  get_id_from_treeview(log_tree)
        if session_log_id == None:
            messagebox.showwarning('No Session Selected', 'Please select session')
            return      
        db.del_session(session_log_id)
        update_task_and_session_display()
        
    except TypeError as e:
        messagebox.showerror('Last Value not of expected type', f'{e}')
    except Exception as e:
        messagebox.showerror('Unexpected exception', f'Unexpected exception {e}')


def fetch_session_logs(selected_project_id) -> list[dict]:   
    session_logs: list[dict] = db.fetch_sessions(selected_project_id)
    return session_logs
    

def update_session_log_display(session_logs) -> None:
    for item in log_tree.get_children():
        log_tree.delete(item)

    for session in session_logs:        
        # format time
        time_spent: int = session['time_spent']        
        hours, minutes, seconds = calculate_hours_minutes_seconds(time_spent)
        formated_time: str = f'{hours:02}h {minutes:02}m {seconds:02}s '        
        
        # assign task_name to id
        task_name:str | None = None
        for item in task_list_tree.get_children():

            task_name_to_id_list: list = task_list_tree.item(item)['values']            
            task_id_in_list:      int  = task_name_to_id_list[-1]
            
            if session['task_id'] == task_id_in_list:
                task_name = task_list_tree.item(item)['values'][1]
                
        if task_name is None:
            task_name = 'unknown task descriptor'

        # add to treeview
        # log_tree_column =  ('Date', 'Duration', 'Task', 'time_spent_in_s', 'task_id', 'session_id')
        # only 'Date', 'Duration', 'Task' displayed
        log_tree.insert('', session['session_id'], values=(session['session_date'],
                                                           formated_time,
                                                           task_name,                                                           
                                                           session['time_spent'],
                                                           session['task_id'],
                                                           session['session_id'])) # session_id needs to be last value for get_id_from_treeview
        

#endregion

#region GUI setup
#window setup
root = tk.Tk()
root.title('time_tracker')
root.geometry('745x600') # width x height
root.resizable(width=False, height=False)

style = Style(theme='solar')
style.configure('.', font=('Helvetica', 12))

top_frame = tk.Frame(root)
#region project UI Elements
#TODO: change fontsize of dropdown
#project display frame
project_display_frame = ttk.Frame(top_frame)
# project_title_combobox
project_name = tk.StringVar(value='Project name')
project_title_combobox = ttk.Combobox(project_display_frame,
                                      textvariable = project_name,
                                      state        = 'readonly',
                                      height       = 5,
                                      postcommand  = click_projects_combobox,
                                      font         = ('Helvetica', 16, 'bold'))
project_title_combobox.bind('<<ComboboxSelected>>', click_update_task_and_session_display)
project_title_combobox.project_dict = dict() #adds project_dict attribute for future reference
# add project button
add_project_button = ttk.Button(project_display_frame,
                                text    = 'Add Project',
                                command = add_project)
# delete project button
delete_project_button = ttk.Button(project_display_frame,
                                   text    = 'delete Project',
                                   command = del_project)

#endregion


#region Timer Button UI Elements
# reset & save frame
frame_reset_save = ttk.Frame(top_frame)
# session_time_button
session_time_button_style = Style()
session_time_button_style.configure('session_time_button_style.TButton',
                                    font=('helvetica', 15, 'bold'))
session_time_button = ttk.Button(frame_reset_save,
                                 style   = 'session_time_button_style.TButton',
                                 width   = 12,                                 
                                 text    = timer_button_default_text,
                                 command = press_timer_button)
# reset_button
reset_button = ttk.Button(frame_reset_save,
                          text    = 'Reset',
                          command = reset)
# save_button
save_button = ttk.Button(frame_reset_save,
                         text    = 'Save',
                         command = add_session)

#endregion


#region total time label UI Elements
# subframe to group total time labels
frame_total_time =ttk.Frame(top_frame)
# total_time_label_name
total_time_label_name = ttk.Label(frame_total_time, width=20, text = 'Total: ')
# total_time_label
total_time_style = Style()
total_time_style.configure('total_time_style.TLabel',
                           font=('helvetica', 15, 'bold'))
total_time = tk.StringVar(value= 'hh:mm:ss')
total_time_label = ttk.Label(frame_total_time,
                             width        = 20,
                             textvariable = total_time,
                             style        = 'total_time_style.TLabel')
#endregion


#region todo list UI Elements
# frame for treeview & scrollbar
task_frame = ttk.LabelFrame(root, text='Tasks')
# task tree frame
task_tree_frame = ttk.Frame(task_frame)
# treeview
task_list_tree_columns: tuple = ('Done: ', 'ToDo: ', 'task_done', 'task_id') # !be carefull changing any of these, display relies  on the order of these
task_list_tree = ttk.Treeview(task_tree_frame,
                              columns    = task_list_tree_columns,
                              show       = "headings",
                              selectmode = "browse",
                              height     = 4)
task_list_tree.heading(column='ToDo: ', text='ToDo: ')
task_list_tree.heading(column='Done: ', text='✓')
task_list_tree.column('ToDo: ', width=650)
task_list_tree.column('Done: ', width=35, anchor=tk.CENTER)
task_list_tree['displaycolumns'] = ('Done: ', 'ToDo: ')
# scrollbar
task_list_scrollbar = ttk.Scrollbar(task_tree_frame,
                                    orient  = tk.VERTICAL,
                                    command = task_list_tree.yview)
task_list_tree.configure(yscrollcommand=task_list_scrollbar.set)
# task button frame
task_button_frame = ttk.Frame(task_frame)
# add task button
add_task_button = ttk.Button(task_button_frame,
                             width   = 10,
                             text    = 'Add Task',                              
                             command = add_task)
# delete task button
delete_task_button = ttk.Button(task_button_frame,
                                width   = 10,
                                text    = 'Delete Task',
                                command = del_task)
# toggle task done button
toggle_task_done_button = ttk.Button(task_button_frame,
                                     width   = 10,
                                     text    = 'Toggle Done',
                                     command = toggle_task_done)

#endregion


#region session log UI Elements
# frame for treeview & scrollbar
log_frame = ttk.Labelframe(root, text='logs')
# log tree & scrollbar frame
log_tree_frame = ttk.Frame(log_frame)
# treeview
log_tree_column:tuple = ('Date: ',
                         'Duration: ',
                         'Task: ',
                         'time_spent_in_s',
                         'task_id',
                         'session_id') # # !be carefull changing any of these, display relies  on the order of these
log_tree = ttk.Treeview(log_tree_frame,
                        columns    = log_tree_column,
                        show       = "headings",
                        selectmode = tk.BROWSE,
                        height     = 5)
log_tree.heading(column='Date: ',     text='Date: ') 
log_tree.heading(column='Duration: ', text='Duration: ') 
log_tree.heading(column='Task: ',     text='Task: ') 
log_tree['displaycolumns'] = ('Date: ', 'Duration: ', 'Task: ')
log_tree.column('Date: '    , width=140, anchor=tk.CENTER)
log_tree.column('Duration: ', width=120, anchor=tk.CENTER)
log_tree.column('Task: ',     width=425, anchor=tk.W)
# scrollbar
log_scrollbar = ttk.Scrollbar(log_tree_frame,
                              orient=tk.VERTICAL,
                              command=log_tree.yview)
log_tree.configure(yscrollcommand=log_scrollbar.set)
#delete session button
delete_session_button = ttk.Button(log_frame,
                                   text    = 'Delete Session',
                                   command = del_session)

#endregion


#region placing GUI elements
top_frame.grid(row=1, column=1, padx=10, pady=10)
# project_display_frame
project_display_frame.grid( row=1, column=1, padx=10, pady=10, sticky=tk.NW)
# Parent: project_display_frame
project_title_combobox.pack(side=tk.TOP,   padx=10, pady=10, fill=tk.X) 
add_project_button.pack(    side=tk.LEFT,  padx=10, pady=10)
delete_project_button.pack( side=tk.RIGHT, padx=10, pady=10)

# reset & save frame
frame_reset_save.grid(row=1, column=2, padx=10, pady=10, sticky=tk.E)
session_time_button.pack(side=tk.LEFT,   padx=10, pady=10, fill=tk.BOTH)
reset_button.pack(       side=tk.BOTTOM, padx=10, pady=10)
save_button.pack(        side=tk.TOP,    padx=10, pady=10)

# frame_total_time
frame_total_time.grid(row=1, column=3, padx=10, pady=10)
total_time_label_name.pack(padx=10, pady=10)
total_time_label.pack(     padx=10, pady=10)

# frame task tree
task_frame.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
task_tree_frame.pack(side=tk.TOP, padx=10, pady=5) # parent: task_frame
# Place  treeview and scrollbar
task_list_tree.pack(     side=tk.LEFT,  fill=tk.BOTH, expand=True)
task_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# task button frame
task_button_frame.pack(side=tk.BOTTOM, padx=5, pady=10, anchor=tk.W) 
add_task_button.grid(        column=1, row=1, sticky=tk.NW, padx=5, pady=5)
delete_task_button.grid(     column=2, row=1, sticky=tk.NE, padx=5, pady=5)
toggle_task_done_button.grid(column=1, row=2, sticky=tk.S,  padx=5, pady=5)

# frame log tree
log_frame.grid(row=3, column=1, padx=10, pady=10,  sticky=tk.W)
log_tree_frame.pack(side=tk.TOP, padx=10, pady=10) # parent: log_frame
# Place  treeview and scrollbar
log_tree.pack(             side=tk.LEFT,  fill=tk.BOTH, expand=True)
log_scrollbar.pack(        side=tk.RIGHT, fill=tk.Y)
delete_session_button.pack(side=tk.BOTTOM, padx=10, pady=5, anchor=tk.W)


#endregion GUI setup