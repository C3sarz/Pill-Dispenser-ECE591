from tkinter import *
import tkinter as tk
from tkinter import ttk
import sys
import time
import RPi.GPIO as GPIO
import threading
import queue


#############################################
#     GPIO Code
#############################################

# set GPIOs for the motor
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
enable_pin = 18; # add the enable pin
coil_A_1_pin = 4 # pink
coil_A_2_pin = 17 # orange
coil_B_1_pin = 23 # blue
coil_B_2_pin = 24 # yellow

# adjust if different
StepCount = 8
Seq = list(range(0, StepCount))
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

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
    
def dispense(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)




    
HEIGHT = 400
WIDTH = 600


class GuiPart:
    #############################################
    #     Clock
    #############################################
    @staticmethod
    def clock(clock_disp, clock_disp1):
        # get the current time
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        ap = time.strftime("%p")
        
        mon = time.strftime("%B")
        d = time.strftime("%d")
        
        clock_disp.config(text=hour + ":" + minute + ":" + second + " " + ap)
        # clock_disp.after(1000, self.clock)
        
        clock_disp1.config(text=mon + "," + d)
        # clock_disp1.after(100000, self.clock)
        #, this will cause freeze problem
        
        # Note: also need to add the function of time interval, number of pills    
        


    #############################################
    #     Scheduling Window
    #############################################


    # Schedule page
    def New_Window(self):
        
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
        
        minute = ttk.Combobox(Window, values=["00", "15", "30", "45", "12", "47"], width=14)
        minute.grid(row=6, column=1)
        minute.current(0)
        
        
        label_am_pm = tk.Label(Window, text ="AM/PM:")
        label_am_pm.grid(row=7, column=0)
        
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
        
        # canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
        # canvas.grid(row=14, column=0)
         
        # def time_check():
                    
        #     current_month = time.strftime("%m")
        #     current_day = time.strftime("%d")
        #     current_hour = time.strftime("%I")
        #     current_ap = time.strftime("%p")
            
        #     if(start_month.get() == "Jan"):
        #         start = 1
        #         start_enday = 31
        #     elif(start_month.get() == "Feb"):
        #         start = 2
        #         start_enday = 28
        #     elif(start_month.get() == "Mar"):
        #         start = 3
        #         start_enday = 31
        #     elif(start_month.get() == "Apr"):
        #         start = 4
        #         start_enday = 30
        #     elif(start_month.get() == "May"):
        #         start = 5
        #         start_enday = 31
        #     elif(start_month.get() == "June"):
        #         start = 6
        #         start_enday = 30
        #     elif(start_month.get() == "July"):
        #         start = 7
        #         start_enday = 31
        #     elif(start_month.get() == "Aug"):
        #         start = 8
        #         start_enday = 31
        #     elif(start_month.get() == "Sep"):
        #         start = 9
        #         start_enday = 30
        #     elif(start_month.get() == "Oct"):
        #         start = 10
        #         start_enday = 31
        #     elif(start_month.get() == "Nov"):
        #         start = 11
        #         start_enday = 30
        #     elif(start_month.get() == "Dec"):
        #         start = 12
        #         start_enday = 31
                
        #     if(end_month.get() == "Jan"):
        #         end = 1
        #         end_enday = 31
        #     elif(end_month.get() == "Feb"):
        #         end = 2
        #         end_enday = 28
        #     elif(end_month.get() == "Mar"):
        #         end = 3
        #         end_enday = 31
        #     elif(end_month.get() == "Apr"):
        #         end = 4
        #         end_enday = 30
        #     elif(end_month.get() == "May"):
        #         end = 5
        #         end_enday = 31
        #     elif(end_month.get() == "June"):
        #         end = 6
        #         end_enday = 30
        #     elif(end_month.get() == "July"):
        #         end = 7
        #         end_enday = 31
        #     elif(end_month.get() == "Aug"):
        #         end = 8
        #         end_enday = 31
        #     elif(end_month.get() == "Sep"):
        #         end = 9
        #         end_enday = 30
        #     elif(end_month.get() == "Oct"):
        #         end = 10
        #         end_enday = 31
        #     elif(end_month.get() == "Nov"):
        #         end = 11
        #         end_enday = 30
        #     elif(end_month.get() == "Dec"):
        #         end = 12
        #         end_enday = 31
                
        #     dispense_onetime = 0  # to make sure only dispense one time      
        #     last_day = 0
        #     current_day = int(time.strftime("%d"))
            
        #     while (last_day==0):
        #         # case when start month is equal to end month
        #         if(int(time.strftime("%m")) == start) and (start == end):
        #             if(int(time.strftime("%d")) >= int(start_day.get())) and (int(time.strftime("%d")) <= int(end_day.get())):
        #                 if(time.strftime("%p") == am_pm.get()):
        #                     if(int(current_hour) == int(hour.get())):
        #                         if(int(time.strftime("%M")) == int(minute.get())):
        #                             # reset dispense check to 0 for a new day
        #                             if(int(time.strftime("%d")) > current_day):
        #                                 current_day += 1
        #                                 dispense_onetime = 0
                                    
        #                             if (dispense_onetime == 0):
        #                                 dispense(3/1000.0, 128)
        #                                 dispense_onetime = 1
                
                
        #         # case when start month is less than end month
        #         elif(int(time.strftime("%m")) == start) and (start < end):
        #             if(int(time.strftime("%d")) >= int(start_day.get())) and (int(time.strftime("%d")) <= start_enday):
        #                 if(time.strftime("%p") == am_pm.get()):
        #                     if(int(current_hour) == int(hour.get())):
        #                         if(int(time.strftime("%M")) == int(minute.get())):
        #                             if(int(time.strftime("%d")) > current_day):
        #                                 current_day += 1
        #                                 dispense_onetime = 0
        #                                 if(start_enday == 31) and (int(time.strftime("%d")) == 31):
        #                                     current_day = 1
        #                                 elif(start_enday == 28) and (int(time.strftime("%d")) == 28):
        #                                     current_day = 1
        #                                 elif(start_enday == 30) and (int(time.strftime("%d")) == 30):
        #                                     current_day = 1 
                                    
        #                             if (dispense_onetime == 0):
        #                                 dispense(3/1000.0, 128)
        #                                 dispense_onetime = 1
                                        
        #         # case when between the start month and end month
                
        #         # add code to update dispense_onetime to 0
        #         elif (int(time.strftime("%m")) > start) and (int(time.strftime("%m")) < end):
        #             if ( (int(time.strftime("%m")) == 1) or (int(time.strftime("%m")) == 3) or (int(time.strftime("%m")) == 5) or (int(time.strftime("%m")) == 7) or (int(time.strftime("%m")) == 8) or (int(time.strftime("%m")) == 10) or (int(time.strftime("%m")) == 12)):
        #                 e_day= 31
        #             elif(int(time.strftime("%m")) == 2):
        #                 e_day = 28
        #             elif((int(time.strftime("%m")) == 4) or (int(time.strftime("%m")) == 6) or (int(time.strftime("%m")) == 9) or (int(time.strftime("%m")) == 11)):
        #                 e_day = 30
                    
        #             if(int(time.strftime("%d")) >= 1) and (int(time.strftime("%d")) <= e_day):
        #                 if(time.strftime("%p") == am_pm.get()):
        #                     if(int(current_hour) == int(hour.get())):
        #                         if(int(time.strftime("%M")) == int(minute.get())):
        #                             if (dispense_onetime == 0):
        #                                 dispense(3/1000.0, 128)
        #                                 dispense_onetime = 1
                                        
        #         # case for the last month                        
        #         elif (start < end) and (int(time.strftime("%m")) == end):
        #             if(int(time.strftime("%d")) >= 1) and (int(time.strftime("%d")) <= int(end_day.get())):
        #                 if(time.strftime("%p") == am_pm.get()):
        #                     if(int(current_hour) == int(hour.get())):
        #                         if(int(time.strftime("%M")) == int(minute.get())):
        #                             if (dispense_onetime == 0):
        #                                 dispense(3/1000.0, 128)
        #                                 dispense_onetime = 1
                    
            # add the above value to database
        
    def confirm():
        confirm_time_start.config(text="Start:" + start_month.get() + "," + start_day.get() + "," + hour.get() + ":" + minute.get() + "," + am_pm.get())
        confirm_time_end.config(text="End:" + end_month.get() + "," + end_day.get() + "," + hour.get() + ":" + minute.get() + "," + am_pm.get())
        self.events.insert((events.size()+1), "Start day:" + start_month.get() + ", " + start_day.get() + ", " + hour.get() + ":" + minute.get() + ", " + am_pm.get() + "   End day:" + end_month.get() + ", " + end_day.get() + ", " + hour.get() + ":" + minute.get() + ", " + am_pm.get() )
        #threading.Thread(target=time_check).start()
            
    def clear_time():
        confirm_time_start.config(text="")
        confirm_time_end.config(text="")
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


    # clear the events in the homepage   
    def clear_text(self):
        self.events.delete(0, END)

    def __init__(self, ws, queue, endCommand):
        self._is_running = True
        self.queue = queue
        # Set up the GUI
        ws.geometry("800x480")
        # ws.attributes("-fullscreen", True)

        # current clock display
        clock_disp = tk.Label(ws, text="", font=("Helvetica", 30), fg="white", bg="black")
        clock_disp.pack()

        # show the exact date
        clock_disp1 = tk.Label(ws, text="", font=("Helvetica", 25), fg="white", bg="black")
        clock_disp1.pack()

        self.clock(clock_disp, clock_disp1)

        space = tk.Label(ws, text=" ")
        space.pack()

        # upcoming events display
        notice = tk.Label(ws, text="Upcoming events", font=("Helvetica", 12))
        notice.pack()

        self.events = tk.Listbox(ws, height = 10, width = 45)
        self.events.pack()


        space_1 = tk.Label(ws, text=" ")
        space_1.pack()

        button_clear = tk.Button(ws, text="Clear events", command=self.clear_text, bg='White', fg='Black')
        button_clear.pack()

        space_2 = tk.Label(ws, text=" ")
        space_2.pack()

        # schedule button jump to the schdule page
        button = tk.Button(ws, text="Schedule", bg='White', fg='Black',
                                      command=lambda:New_Window())

        button.pack()

        close_main = tk.Button(ws, text="Close", command=endCommand, bg='White', fg='Black')
        close_main.pack()
        # self._is_running = False

    def processIncoming(self, gui):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                gui.events.insert((gui.events.size()+1),msg)
                print(msg)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                print("q empty")
                pass



class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(self.gui)
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            print("GUI dying!")
            self.master.destroy()
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            time.sleep(1)
            msg = "test"
            self.queue.put(msg)
        print("worker dying")

    def endApplication(self):
        print("end command sent")
        self.running = 0

#############################################
#     Main
#############################################

print("start")
ws = tk.Tk()
ws.title("Home Page")

client = ThreadedClient(ws)

print("starting loop")
ws.mainloop()
print("loop done")

print("threads alive: " + str(client.thread1.is_alive()))
client.endApplication()

