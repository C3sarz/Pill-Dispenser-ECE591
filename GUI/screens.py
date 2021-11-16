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
    Window.attributes("-fullscreen", True)
    
    google_cal = tk.Button(Window, text="Google Calendar")
    google_cal.grid(row=0, column=0)
    
    label_month = tk.Label(Window, text="Month:")
    label_month.grid(row=1, column=0)
    
    month = ttk.Combobox(Window, values=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], width = 9)
    month.grid(row=1, column=1)
    month.current(0)

    label_day = tk.Label(Window, text="Day:")
    label_day.grid(row=2, column=0)
    
    day = ttk.Combobox(Window, values=["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"], width = 9)
    day.grid(row=2, column=1)
    day.current(0)
    
    label_time = tk.Label(Window, text="Hour:")
    label_time.grid(row=3, column=0)
    
    hour = ttk.Combobox(Window, values=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12"], width = 9)
    hour.grid(row=3, column=1)
    hour.current(0)
    
    label_minute = tk.Label(Window, text="Minute:")
    label_minute.grid(row=4, column=0)
    
    minute = ttk.Combobox(Window, values=["00", "15", "30", "45"], width=9)
    minute.grid(row=4, column=1)
    minute.current(0)
    
    
    am_pm = tk.Label(Window, text ="AM/PM:")
    am_pm.grid(row=5, column=0)
    
    am_pm = ttk.Combobox(Window, values=["AM", "PM"], width=9)
    am_pm.grid(row=5, column=1)
    am_pm.current(0)
    
    label_repeat = tk.Label(Window, text="Repeatability")
    label_repeat.grid(row=6, column=0)
    
    repeat = ttk.Combobox(Window, values=["1 time a day", "2 times a day", "3 times a day"], width=9)
    repeat.grid(row=6, column=1)

    label_number = tk.Label(Window, text="Number of pills")
    label_number.grid(row=7, column=0)
    
    numberOfPills = ttk.Combobox(Window, values=["1", "2", "3", "4", "5"], width=9)
    numberOfPills.grid(row=7, column=1)

    close = tk.Button(Window, text="Back", command=Window.destroy)
    close.grid(row=8, column=0)
    
    
    # once click the confirm button, get values from all combobox to get the scheduled time
    confirm = tk.Button(Window, text="Confirm")
    confirm.grid(row=9, column=1)
    
    # add the command for clear button to set all values to default values
    clear = tk.Button(Window, text="Clear")
    clear.grid(row=9, column=0)
    
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.grid(row=10, column=0)
    
def clear_text():
    events.delete(0, END)

HEIGHT = 300
WIDTH = 500

ws = tk.Tk()
ws.title("Home Page")
ws.geometry("800x480")
ws.attributes("-fullscreen", True)

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

close_main = tk.Button(ws, text="Close", command=ws.destroy, bg='White', fg='Black')
close_main.pack()

# canvas pack
canvas = tk.Canvas(ws, height=300, width=600)
canvas.pack()


ws.mainloop()
