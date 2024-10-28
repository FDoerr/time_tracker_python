import tkinter as tk
from tkinter import ttk
import sv_ttk #https://github.com/rdbende/Sun-Valley-ttk-theme

from timer import Timer
#TODO: change to this style: https://ttkbootstrap.readthedocs.io/en/version-0.5/tutorial.html
#TODO: editable Treeview cells: https://www.youtube.com/watch?v=n5gItcGgIkk
#TODO: total time spent label functionality

# global variables
timer_button_default_text: str = 'start timer'

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
        update_display()

def update_display() -> None:
    if timer.running:
        elapsed_time = timer.get_elapsed_time()        
        hours, minutes, seconds = calculate_hours_minutes_seconds(elapsed_time)
        session_time_button.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        root.after(500, update_display) #call function after 500ms, keeps UI Responsive

def calculate_hours_minutes_seconds(elapsed_time_in_s:int) -> tuple[int, int, int]:
    hours   = int( elapsed_time_in_s / 3600)  
    minutes = int((elapsed_time_in_s % 3600) / 60)  
    seconds = int(elapsed_time_in_s  % 60)
    return hours, minutes, seconds
 #endregion

#region project related functions
#TODO
def add_project():
    ...

def del_project():
    ...

def select_project():
    ...

def fetch_projects():
    ...

def update_projects_display():
    ...

#endregion

#region task list related functions
#TODO
def add_task():
    ...

def del_task():
    ...

def fetch_tasks():
    ...

def update_task_display():
    ...
#endregion

#region session log related functions
#TODO
def add_session_log():
    ...

def del_session_log():
    ...

def fetch_session_logs():
    ...

def update_session_log_display():
    ...
#endregion

#region GUI

# window setup
root = tk.Tk()
sv_ttk.use_dark_theme()
root.title('time_tracker')
root.geometry('675x475') #width x height
root.minsize(width=400, height=300)

#project display frame
project_display_frame = ttk.Frame(root)
project_display_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.NW)
# project_title_combobox
project_name = tk.StringVar(value= 'Project name')
project_title_combobox = ttk.Menubutton(project_display_frame, textvariable = project_name, state='readonly')
project_title_combobox.pack(side=tk.LEFT, padx=10)
# add project button
add_project_button = ttk.Button(project_display_frame, text='Add Project')
add_project_button.pack(side=tk.LEFT, padx=10)
# delete project button
delete_project_button = ttk.Button(project_display_frame, text='delete Project')
delete_project_button.pack(side=tk.LEFT, padx=10)

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


# todo list
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
add_task_button = ttk.Button(task_button_frame, text='Add Task')
add_task_button.pack(side=tk.LEFT, padx=5, pady=5)
# delete task button
delete_task_button = ttk.Button(task_button_frame, text='Delete Task')
delete_task_button.pack(side=tk.RIGHT, padx=5, pady=5)


# session log
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
delete_session_button = ttk.Button(log_frame, text = 'Delete Session')
delete_session_button.pack(side=tk.BOTTOM, padx=5, pady=5)

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
save_button = ttk.Button(frame_reset_save, text = 'Save')
save_button.pack(side=tk.TOP, padx = 10, pady = 10)


#endregion