from tkinter import *
import tkinter as tk
from tkinter import ttk
import time

def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    
    my_label.config(text=hour + ":" + minute + ":" + second)
    my_label.after(1000, clock)
    
    
# new window to set up the schedule    
def New_Window():
    Window = tk.Toplevel()
    Window.title('Schedule Window')
    
    google_cal = tk.Button(Window, text="Google Calendar")
    google_cal.grid(row=0, column=0)
    
    label_month = tk.Label(Window, text="Month:")
    label_month.grid(row=1, column=0)
    
    month = ttk.Combobox(Window, values=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], width = 9)
    month.grid(row=1, column=1)

    label_day = tk.Label(Window, text="Day:")
    label_day.grid(row=2, column=0)
    
    day = ttk.Combobox(Window, values=["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"], width = 9)
    day.grid(row=2, column=1)
    
    label_time = tk.Label(Window, text="Time:")
    label_time.grid(row=3, column=0)
    
    hour = ttk.Combobox(Window, values=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    hour.grid(row=3, column=1)
    
    minute = ttk.Combobox(Window, values=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "12", "1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    
    close = tk.Button(Window, text='Close', command=Window.destroy).pack(expand=True)
    
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.pack()
def clear_text():
    events.delete(0, END)

HEIGHT = 300
WIDTH = 500

ws = tk.Tk()
ws.title("Home Page")

# current clock display
my_label = tk.Label(ws, text="", font=("Helvetica", 30), fg="white", bg="black")
my_label.pack()

clock()

space = tk.Label(ws, text=" ")
space.pack()

# upcoming events display
notice = tk.Label(ws, text="Upcoming events", font=("Helvetica", 12))
notice.pack()

events = tk.Listbox(ws, height = 10, width = 25)
events.pack()
events.insert(1, "Day Month Time")


space_1 = tk.Label(ws, text=" ")
space_1.pack()

button_clear = tk.Button(ws, text="Clear events", command=clear_text, bg='White', fg='Black')
button_clear.pack()

space_2 = tk.Label(ws, text=" ")
space_2.pack()

# schedule button jump to the schdule page
button = tk.Button(ws, text="Schedule", bg='White', fg='Black',
                              command=lambda:New_Window())

button.pack()

# canvas pack
canvas = tk.Canvas(ws, height=300, width=600)
canvas.pack()

ws.mainloop()
