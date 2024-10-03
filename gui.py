import tkinter
from tkinter import ttk
import sv_ttk #https://github.com/rdbende/Sun-Valley-ttk-theme

root = tkinter.Tk()

button = ttk.Button(root, text="Button")
button.pack()

sv_ttk.use_dark_theme()

root.mainloop() 