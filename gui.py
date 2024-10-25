import tkinter as tk
from tkinter import ttk
import sv_ttk #https://github.com/rdbende/Sun-Valley-ttk-theme

from timer import Timer
#TODO: task/todo-list -> treeview
#TODO: Session Log -> treeView https://www.youtube.com/watch?v=n5gItcGgIkk
#TODO: total time spent label functionality

# global variables
timer_button_default_text: str = 'start timer'

# initialization
timer:Timer =Timer() 


#region Stopwatch button related functions
def reset():
    timer.stop()
    timer.reset()
    session_time_button.config(text=timer_button_default_text)

def press_timer_button():
    if timer.running:
        timer.stop()
    else:
        timer.start()
        update_display()

def update_display():
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


#region GUI

# window setup
root = tk.Tk()
sv_ttk.use_dark_theme()
root.title('time_tracker')
root.geometry('400x300')
root.minsize(width=400, height=300)


# project_title_combobox
project_name = tk.StringVar(value= 'Project name')
project_title_combobox = ttk.Combobox(root, textvariable = project_name)
project_title_combobox.grid(row=1, column=1, padx=10, pady=10)


# subframe to group total time labels
frame_total_time =ttk.Frame(root)
frame_total_time.grid(row=2, column=1, padx = 10, pady = 10)
# total_time_label_name
total_time_label_name = ttk.Label(frame_total_time, text = 'Total: ')
total_time_label_name.grid(row=3, column=1,  padx = 10, pady = 10)
# total_time_label
total_time = tk.StringVar(value= 'dd:hh:mm:ss')
total_time_label = ttk.Label(frame_total_time, textvariable = total_time)
total_time_label.grid(row=4, column=1,  padx = 10, pady = 10)


# todo list
# frame for treeview & scrollbar
task_frame = ttk.Frame(root)
task_frame.grid(row=5, column=1, padx=10, pady=10)
# treeview
task_list_tree_columns = ('ToDo: ',)
task_list_tree = ttk.Treeview(task_frame, columns=task_list_tree_columns, show="headings", selectmode="browse", height=8)
task_list_tree.heading(column='ToDo: ', text='ToDo: ')
# scrollbar
task_list_scrollbar = ttk.Scrollbar(task_frame, orient=tk.VERTICAL, command=task_list_tree.yview)
task_list_tree.configure(yscrollcommand=task_list_scrollbar.set)
# Place the Treeview and scrollbar
task_list_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
task_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# session_time_button
session_time_button = ttk.Button(root, text = timer_button_default_text , command = press_timer_button)
session_time_button.grid(row= 1, column=3, padx = 10, pady = 10)


# reset & save frame
frame_reset_save = ttk.Frame(root)
frame_reset_save.grid(row=2, column=3, padx=10, pady=10)

# reset_button
reset_button = ttk.Button(frame_reset_save, text = 'reset', command = reset)
reset_button.grid(row= 2, column=3, padx = 5, pady = 5)

# save_button
save_button = ttk.Button(frame_reset_save, text = 'save')
save_button.grid(row= 3, column=3, padx = 5, pady = 5)
#endregion