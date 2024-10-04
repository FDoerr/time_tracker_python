import tkinter as tk
from tkinter import ttk
import sv_ttk #https://github.com/rdbende/Sun-Valley-ttk-theme

# window setup
root = tk.Tk()
sv_ttk.use_dark_theme()
root.title('time_tracker')
root.geometry('400x150')
root.minsize(width=400, height=150)


# left frame
frame_left = ttk.Frame(root)
frame_left.pack(side='left', fill='x', padx = 10, pady = 10)
# project_title_combobox
project_name = tk.StringVar(value= 'Project name')
project_title_combobox = ttk.Combobox(frame_left, textvariable = project_name)
project_title_combobox.pack(side='top', fill='x', padx = 10, pady = 10)


# subframe in left frame to group labels
frame_total_time =ttk.Frame(frame_left)
frame_total_time.pack(side='left', fill='x', padx = 10, pady = 10)
# total_time_label_name
total_time_label_name = ttk.Label(frame_total_time, text = 'Total: ')
total_time_label_name.pack(side='left',  padx = 10, pady = 10)
# total_time_label
total_time = tk.StringVar(value= 'dd:hh:mm:ss')
total_time_label = ttk.Label(frame_total_time, textvariable = total_time)
total_time_label.pack(side='right',  padx = 10, pady = 10)




# right frame
frame_right = ttk.Frame(root)
frame_right.pack(side='right', padx = 10, pady = 10)
# session_time_button
session_time = tk.StringVar(value= 'hh:mm:ss')
session_time_button = ttk.Button(frame_right, textvariable = session_time)
session_time_button.pack(side='top', padx = 10, pady = 10)


# save_button
save_button = ttk.Button(frame_right, text = 'save')
save_button.pack(side='top', padx = 10, pady = 10)


# for item in session_time_button.keys():
#     print(item,': ', session_time_button[item])

root.mainloop() 