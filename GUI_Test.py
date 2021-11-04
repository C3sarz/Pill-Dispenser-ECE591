from Tkinter import *
# import the needed modules from Tkinter
import tkFont
import tkMessageBox
import ttk
import RPi.GPIO as GPIO
import time
import calendar
import tkinter as tk

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
enable_pin = 18; # add the enable pin
coil_A_1_pin = 4 # pink
coil_A_2_pin = 17 # orange
coil_B_1_pin = 23 # blue
coil_B_2_pin = 24 # yellow

# adjust if different
# adjust if different
StepCount = 8
Seq = range(0, StepCount)
Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0]
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]

GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

GPIO.output(enable_pin, 1)

# create our main window
win = Tk()

# define the Font
myFont = tkFont.Font(family = 'Helvetica', size = 20, weight = 'bold')

class Window(tk.Toplevel)
    def __init__(self, parent):
        super().__init__(parent)
        
        self.geometry('300x100')
        self.title('Toplevel window')
        
        ttk.Button(self, text="Close", command=self.destroy).pack(expand=True)
        
class App(tk.Tk):
    def __int__(self):
        super().__init__()
        
        self.geometry('300x200')
        self.title('Main window')
        ttk.Button(self, text="open a window", command=self.open_window).pack(expand=True)
        
    def open_window(self):
        window = Window(self)
        window.grab_set()

# define the GPIO for motor
def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

# define the function to make motor move clockwise
def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

# define the function to make motor move counterclockwise
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

# define the function for the dispensing button to change text
def textChange():
    print("Pill is dispensing")
    result = tkMessageBox.askquestion(title = 'Confirm', message = 'Are you sure?')
   
    # if the result is yes, rotate the motor to dispense pills
    if result == 'yes':
        forward(3/1000.0, 426)
        tkMessageBox.showinfo('test', 'Finished')
        # delay = raw_input("Time Delay (ms)?")
        # steps = raw_input("How many steps forward? ")
        # steps = raw_input("How many steps backwards? ")
        # backwards(int(delay) / 1000.0, int(steps))
    # if the result is no, do nothing
    else:
        tkMessageBox.showinfo('test', 'Wrong')
        


win.title("Test GUI")
win.geometry('1000x600')

#Create a button
testButton = Button(win, text = "Dispense", command = textChange, font = myFont, height = 2, width = 6)

# Put button at the top position, other positions: LEFT, RIGHT, BOTTOM
testButton.grid(row = 2, column = 6)

# create the schedule GUI to let user input their schedule
# there is an error after click the button to dispense
label = Label(win, text="Set your schedule: ")
label.grid(row = 0, column = 0)

label = Label(win, text="Day: ")
label.grid(row = 1, column = 0)

label = Label(win, text="Time: ")
label.grid(row = 2, column = 0)

year = ttk.Combobox(win, values = ["2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"], width = 7)
year.grid(row = 1, column = 1)

month = ttk.Combobox(win, values = ["Jau", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], width = 7)
month.grid(row = 1, column = 2)

day = ttk.Combobox(win, values = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], width = 7)
day.grid(row = 1, column = 3)

# have the same name with the time which caused the issue that dispensing wont work
#time_schedule = Entry(win)
#time_schedule.grid(row = 2, column = 1)

time_d1 = ttk.Combobox(win, values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], width = 7)
time_d1.grid(row = 2, column = 1)
# add corresponding buttons for each digit(two buttons), using the increase/decrease functions defined

time_d2 = ttk.Combobox(win, values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], width = 7)
time_d2.grid(row = 2, column = 2)

mid_label = Label(win, text = ":", width = 2)
mid_label.grid(row = 2, column = 3)

time_d3 = ttk.Combobox(win, values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], width = 7)
time_d3.grid(row = 2, column = 4)

time_d4 = ttk.Combobox(win, values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], width = 7)
time_d4.grid(row = 2, column = 5)

c = calendar.TextCalendar(calendar.THURSDAY)
str = c.formatmonth(2025, 1)
print(str)

window = 

d1 = time_d1.get()
d2 = time_d2.get()
d3 = time_d3.get()
d4 = time_d4.get()

mainloop()