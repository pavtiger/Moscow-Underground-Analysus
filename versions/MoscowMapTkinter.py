# PavelArtiushkov
# 22.09.2018.
# MoscowMetroMapPoppularity
 
from tkinter import *

tk=Tk()
tk.title('METRO')
tk.geometry('1024x721')
im = PhotoImage(file='C:/Users/Pavel/Downloads/MainMap.gif')
l = Label(tk, image=im)
l.pack(fill='x', expand=True)
 
tk.mainloop()