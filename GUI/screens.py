from tkinter import *
import tkinter as tk
from tkinter import ttk
import time

def clock():
    # get the current time
    hour = time.strftime("%I")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    ap = time.strftime("%p")
    
    mon = time.strftime("%B")
    d = time.strftime("%d")
    
    my_label.config(text=hour + ":" + minute + ":" + second + " " + ap)
    my_label.after(1000, clock)
    
    my_label1.config(text=mon + "," + d)
    #my_label1.after(1000, clock), this will cause freeze problem
    
    

# new window to set up the schedule    
def New_Window():
    
    def confirm():
        confirm_time_start.config(text="Start:" + start_month.get() + "," + start_day.get() + "," + hour.get() + ":" + minute.get() + "," + am_pm.get())
        confirm_time_end.config(text="End:" + end_month.get() + "," + end_day.get() + "," + hour.get() + ":" + minute.get() + ", " + am_pm.get())
        events.insert((events.size()+1), "Start day:" + start_month.get() + ", " + start_day.get() + ", " + hour.get() + ":" + minute.get() + ", " + am_pm.get() + "   End day:" + end_month.get() + ", " + end_day.get() + ", " + hour.get() + ":" + minute.get() + ", " + am_pm.get() )
        # add the above value to database
        
    def clear_time():
        confirm_time.config(text="")
        # remove the time string from the database
    
    def change_startdays():
        # different number of days of months
        if( (start_month.get()=="Jan") or (start_month.get()=="Mar") or (start_month.get()=="May") or (start_month.get()=="July") or (start_month.get()=="Aug") or (start_month.get()=="Oct") or (start_month.get()=="Dec") ):
            s_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
        elif(start_month.get()=="Feb"):
            s_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
        elif((start_month.get()=="Apr") or (start_month.get()=="June") or (start_month.get()=="Sep") or (start_month.get()=="Nov")):
            s_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
            
        start_day.config(values=s_days)
        start_day.after(200, change_startdays)
    
    def change_enddays():
        # different number of days of months
        if( (end_month.get()=="Jan") or (end_month.get()=="Mar") or (end_month.get()=="May") or (end_month.get()=="July") or (end_month.get()=="Aug") or (end_month.get()=="Oct") or (end_month.get()=="Dec") ):
            e_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
        elif(end_month.get()=="Feb"):
            e_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
        elif((end_month.get()=="Apr") or (end_month.get()=="June") or (end_month.get()=="Sep") or (end_month.get()=="Nov")):
            e_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
            
        end_day.config(values=e_days)
        end_day.after(200, change_enddays)


    # open up a new window
    Window = tk.Toplevel()
    Window.title('Schedule Window')
    Window.attributes("-fullscreen", True)
    
    google_cal = tk.Button(Window, text="Google Calendar")
    google_cal.grid(row=0, column=0)
    
    # start day of the schedule
    label_startmonth = tk.Label(Window, text="Start Month:")
    label_startmonth.grid(row=1, column=0)
    
    start_month = ttk.Combobox(Window, values=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], width = 14)
    start_month.grid(row=1, column=1)
    start_month.current(0)

    label_startday = tk.Label(Window, text="Start Day:")
    label_startday.grid(row=2, column=0)
    
    start_day = ttk.Combobox(Window, width=14)
    start_day.grid(row=2, column=1)
    
    change_startdays()
    
    # end day of the schedule
    
    label_endmonth = tk.Label(Window, text="End Month:")
    label_endmonth.grid(row=3, column=0)
    
    end_month = ttk.Combobox(Window, values=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], width = 14)
    end_month.grid(row=3, column=1)
    end_month.current(0)
    
    label_endday = tk.Label(Window, text="End Day:")
    label_endday.grid(row=4, column=0)
    
    end_day = ttk.Combobox(Window, width=14)
    end_day.grid(row=4, column=1)    
    
    change_enddays()
    
    # set up the hour
    label_time = tk.Label(Window, text="Hour:")
    label_time.grid(row=5, column=0)
        
    hour = ttk.Combobox(Window, values=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12"], width=14)
    hour.grid(row=5, column=1)
    hour.current(0)
    
    label_minute = tk.Label(Window, text="Minute:")
    label_minute.grid(row=6, column=0)
    
    minute = ttk.Combobox(Window, values=["00", "15", "30", "45"], width=14)
    minute.grid(row=6, column=1)
    minute.current(0)
    
    
    am_pm = tk.Label(Window, text ="AM/PM:")
    am_pm.grid(row=7, column=0)
    
    am_pm = ttk.Combobox(Window, values=["AM", "PM"], width=14)
    am_pm.grid(row=7, column=1)
    am_pm.current(0)
    
    label_repeat = tk.Label(Window, text="Time Interval")
    label_repeat.grid(row=8, column=0)
    
    repeat = ttk.Combobox(Window, values=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], width=14)
    repeat.grid(row=8, column=1)
    repeat.current(0)

    label_number = tk.Label(Window, text="Number of pills")
    label_number.grid(row=9, column=0)
    
    numberOfPills = ttk.Combobox(Window, values=["1", "2", "3", "4", "5"], width=14)
    numberOfPills.grid(row=9, column=1)
    numberOfPills.current(0)

    close = tk.Button(Window, text="Back", command=Window.destroy)
    close.grid(row=10, column=0)
    
    
    # once click the confirm button, get values from all combobox to get the scheduled time
    confirm = tk.Button(Window, text="Confirm", command=confirm)
    confirm.grid(row=11, column=1)
    
    # add the command for clear button to set all values to default values
    clear = tk.Button(Window, text="Clear", command=clear_time)
    clear.grid(row=11, column=0)
    
    confirm_time_start = tk.Label(Window, text="")
    confirm_time_start.grid(row=12, column=1)
    
    confirm_time_end = tk.Label(Window, text="")
    confirm_time_end.grid(row=13, column=1)
    
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.grid(row=14, column=0)
    
    
def clear_text():
    events.delete(0, END)
    
HEIGHT = 400
WIDTH = 600

ws = tk.Tk()
ws.title("Home Page")
ws.geometry("800x480")
ws.attributes("-fullscreen", True)

# current clock display
my_label = tk.Label(ws, text="", font=("Helvetica", 30), fg="white", bg="black")
my_label.pack()

# show the exact date
my_label1 = tk.Label(ws, text="", font=("Helvetica", 25), fg="white", bg="black")
my_label1.pack()

clock()

space = tk.Label(ws, text=" ")
space.pack()

# upcoming events display
notice = tk.Label(ws, text="Upcoming events", font=("Helvetica", 12))
notice.pack()

events = tk.Listbox(ws, height = 10, width = 45)
events.pack()


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
