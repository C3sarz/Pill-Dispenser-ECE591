import tkinter as tk
import time

def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    
    my_label.config(text=hour + ":" + minute + ":" + second)
    my_label.after(1000, clock)
    
def update():
    my_label.config(text="New Text")

# new window to control the calendar
def New_Window():
    Window = tk.Toplevel()
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.pack()
    
    
HEIGHT = 300
WIDTH = 500

ws = tk.Tk()
ws.title("Python Guides")
canvas = tk.Canvas(ws, height=HEIGHT, width=WIDTH)
canvas.pack()

button = tk.Button(ws, text="Schedule", bg='White', fg='Black',
                              command=lambda: New_Window())


button.pack()

my_label = tk.Label(ws, text="", font=("Helvetica", 48), fg="green", bg="black")
my_label.pack()

clock()
ws.mainloop()