from __future__ import print_function
from tkinter import *
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
import sys
import time
import RPi.GPIO as GPIO
import threading
import queue
import datetime

# Google Calendar Libraries
import os.path
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import textwrap
import uuid

# BLE-related libraries
from bluepy import btle
import binascii

months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthDict = {
    "Jan":1,
    "Feb":2,
    "Mar":3,
    "Apr":4,
    "May":5,
    "June":6,
    "July":7,
    "Aug":8,
    "Sep":9,
    "Oct":10,
    "Nov":11,
    "Dec":12
}
bracelet_MAC_address = ""
currentlyDispensing = False
dispenseTimer = 0
dispensedPills = 0
currentItem = []

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

#############################################
#     GPIO Code
#############################################

# GPIO Setup and pin assignments
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
motor_enable_pin = 18; # enable pin
coil_A_1_pin = 4 # pink
coil_A_2_pin = 17 # orange
coil_B_1_pin = 23 # blue
coil_B_2_pin = 24 # yellow

# Peripheral Pins
buzzer_pin = 13 # PWM Channel 1 Buzzer Pin
laser_pin = 25 # Pin to control the tripwire laser
chamber_led_pin = 9 # Pin to control the cylinder chamber LED
tripwire_input_pin  = 26 # Boolean input of the tripwire status
chamber_led_input_pin = 8 # Boolean input of the verification chamber status
enable_pin = 6

# GPIO Pin configuration
GPIO.setup(motor_enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(laser_pin, GPIO.OUT)
GPIO.setup(chamber_led_pin, GPIO.OUT)
GPIO.setup(tripwire_input_pin, GPIO.IN)
GPIO.setup(chamber_led_input_pin, GPIO.IN)

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

 
GPIO.output(motor_enable_pin, 1)

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
    

# Returns all event entries on the database.
def readDatabase(fileName):
    events = []
    file = open(fileName, 'r')
    line = file.readline().rstrip()

    while line != '-' and line != '':
        if line == '*':
            newItem = dispenseItem(file.readline().rstrip(), int(file.readline().rstrip()), int(file.readline().rstrip()), int(file.readline().rstrip()), file.readline().rstrip())
            line = file.readline().rstrip()
            print("Appending eventID: " + newItem.cal_id)
            events.append(newItem)
        else:
            line = file.readline().rstrip()

    file.close()
    return events

# Updates the database, adding or deleting items.
def updateDatabase(fileName, events):
    print('+++ Updating Database! +++')
    file = open(fileName, 'w')

    for item in events:
        if not item.google_cal:
            file.write('*\n')
            file.write(item.cal_id + '\n')
            file.write(str(item.start_year) + '\n')
            file.write(str(item.start_month) + '\n')
            file.write(str(item.start_day) + '\n')
            file.write((item.dispenseTime) + '\n')
            file.write('.\n')
            file.write(str(False) + '\n')
            file.write(str(item.numberOfPills) + '\n')
            file.write(str(item.repetition) + '\n')
            file.write(str(item.end_year) + '\n')
            file.write(str(item.end_month) + '\n')
            file.write(str(item.end_day) + '\n')
    file.write('-')
    file.close()

class dispenseItem:
    def __init__(self, cal_id, start_year, start_month, start_day, dispenseTime, google_cal = False, numberOfPills = 1, repetition = 0, end_year=0, end_month = 0, end_day = 0):
        self.cal_id = cal_id
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.dispenseTime = dispenseTime
        self.google_cal = google_cal

        self.numberOfPills = numberOfPills
        self.repetition = repetition

        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day


class GuiPart:
    #############################################
    #     Clock
    #############################################
    def clock(self):
        # get the current time
        hour = time.strftime("%I")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        ap = time.strftime("%p")
        
        mon = time.strftime("%B")
        d = time.strftime("%d")
        
        self.clock_disp.config(text=hour + ":" + minute + ":" + second + " " + ap)        
        self.clock_disp1.config(text=mon + " " + d)
        self.clock_disp.after(1000, self.clock)
        

    def arrowButtons(self, row, direction):
        if row == 0:
            if direction == 'up' and monthDict[self.start_month.get()] <= 11:
                self.start_month.current(monthDict[self.start_month.get()])
            elif direction == 'down' and monthDict[self.start_month.get()]-2 >= 0:
                self.start_month.current(monthDict[self.start_month.get()]-2)
        elif row == 1:
            if direction == 'up' and int(self.start_day.get())-1 <= len(self.start_day['values'])-1:
                self.start_day.current(int(self.start_day.get())-1)
            elif direction == 'down' and int(self.start_day.get())-3 >= 0:
                self.start_day.current(int(self.start_day.get())-3)
        elif row == 2:
            if direction == 'up' and monthDict[self.end_month.get()] <= 11:
                self.end_month.current(monthDict[self.end_month.get()])
            elif direction == 'down' and monthDict[self.end_month.get()]-2 >= 0:
                self.end_month.current(monthDict[self.end_month.get()]-2)
        elif row == 3:
            if direction == 'up' and int(self.end_day.get())-1 <= len(self.end_day['values'])-1:
                self.end_day.current(int(self.end_day.get())-1)
            elif direction == 'down' and int(self.end_day.get())-3 >= 0:
                self.end_day.current(int(self.end_day.get())-3)
        elif row == 4:
            if direction == 'up' and int(self.hour.get()) <= 11:
                self.hour.current(int(self.hour.get()))
            elif direction == 'down' and int(self.hour.get())-2 >= 0:
                self.hour.current(int(self.hour.get())-2)
        elif row == 5:
            newMin = int(self.minute.get())
            if direction == 'up':
                if newMin == 0:
                    self.minute.current(1)
                elif newMin == 15:
                    self.minute.current(2)
                elif newMin == 30:
                    self.minute.current(3)
                elif newMin == 45:
                    self.minute.current(4)
            elif direction == 'down':
                if newMin == 0:
                    self.minute.current(0)
                elif newMin == 15:
                    self.minute.current(0)
                elif newMin == 30:
                    self.minute.current(1)
                elif newMin == 45:
                    self.minute.current(2)
                else:
                    self.minute.current(3)
        elif row == 6:
            if direction == 'up':
                self.am_pm.current(1)
            elif direction == 'down':
                self.am_pm.current(0)
        elif row == 7:
            if direction == 'up' and int(self.repeat.get())+1 <= 11:
                self.repeat.current(int(self.repeat.get())+1)
            elif direction == 'down' and int(self.repeat.get())-1 >= 0:
                self.repeat.current(int(self.repeat.get())-1)
        elif row == 8:
            if direction == 'up' and int(self.pills.get()) <= 4:
                self.pills.current(int(self.pills.get()))
            elif direction == 'down' and int(self.pills.get())-2 >= 0:
                self.pills.current(int(self.pills.get())-2)


    #############################################
    #     Dispensing Window
    #############################################
        
    def dispenseWindow(self):
        myFont_w = font.Font(size=21)
        Window = tk.Toplevel()
        Window.title('Dispense Window')
        Window.attributes("-fullscreen", True)

        close = tk.Button(Window, text="Back", command=Window.destroy, height=2, width=13)
        close['font'] = myFont_w
        close.grid(row=1, column=0)
        
        number = tk.Label(Window, text="Number of Pills: ", height=5, width=13)
        number['font'] = myFont_w
        number.grid(row=1, column=1)
        
        amount = self.pills.get()
        numberOfPills = tk.Text(Window, height = 8, width=13)
        numberOfPills.insert(tk.END, amount)
        numberOfPills['font'] = myFont_w
        numberOfPills.grid(row=2, column=1)
        
        chamber_label = tk.Label(Window, text="Chamber Test", height=5, width=13)
        chamber_label['font'] = myFont_w
        chamber_label.grid(row=1, column=2)
        
        chamber_test = tk.Text(Window, height=8, width=13)
        chamber_test['font'] = myFont_w
        chamber_test.grid(row=2, column=2)
        
        tripWire_label = tk.Label(Window, text="Trip Wire Test", height=5, width=13)
        tripWire_label['font'] = myFont_w
        tripWire_label.grid(row=1, column=3)
        
        tripWire_test = tk.Text(Window, height=8, width=13)
        tripWire_test['font'] = myFont_w
        tripWire_test.grid(row=2, column=3)
        

    #############################################
    #     Scheduling Window
    #############################################
    def scheduleWindow(self):
        
        # open up a new window
        myFont_w = font.Font(size=16)
        
        # open up a new window
        Window = tk.Toplevel()
        Window.title('Schedule Window')
        Window.attributes("-fullscreen", True)
        
        
        google_cal = tk.Button(Window, text="Google Calendar", height = 2, width = 16)
        google_cal['font'] = myFont_w
        google_cal.grid(row=0, column=0)
        
        
        # start day of the schedule
        label_startmonth = tk.Label(Window, text="Start Month:", height = 2, width = 14)
        label_startmonth['font'] = myFont_w
        label_startmonth.grid(row=0, column=1)

        
        self.start_month = ttk.Combobox(Window, values=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], height = 9, width = 14)
        self.start_month['font'] = myFont_w
        self.start_month.grid(row=0, column=2)
        self.start_month.current(int(time.strftime("%m"))-1)
        
        button_0_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(0, 'down'))
        button_0_0 ['font'] = myFont_w
        button_0_0.grid(row = 0, column = 3)
        
        button_0_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(0, 'up'))
        button_0_1.grid(row = 0, column = 4)
        button_0_1 ['font'] = myFont_w

        label_startday = tk.Label(Window, text="Start Day:", height = 2, width = 14)
        label_startday['font'] = myFont_w
        label_startday.grid(row=1, column=1)
        
        self.start_day = ttk.Combobox(Window, height = 9, width=14)
        self.start_day['font'] = myFont_w
        self.start_day.grid(row=1, column=2)
        
        self.change_startdays()        
        self.start_day.current(int(time.strftime("%d"))-2)
        
        button_1_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(1, 'down'))
        button_1_0 ['font'] = myFont_w
        button_1_0.grid(row = 1, column = 3)
        
        button_1_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(1, 'up'))
        button_1_1 ['font'] = myFont_w
        button_1_1.grid(row = 1, column = 4)
        
        # end day of the schedule
        
        label_endmonth = tk.Label(Window, text="End Month:", height=2, width=14)
        label_endmonth['font'] = myFont_w
        label_endmonth.grid(row=2, column=1)
        
        self.end_month = ttk.Combobox(Window, values=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"], height = 9, width = 14)
        self.end_month['font'] = myFont_w
        self.end_month.grid(row=2, column=2)
        self.end_month.current(int(time.strftime("%m"))-1)
        
        button_2_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(2, 'down'))
        button_2_0 ['font'] = myFont_w
        button_2_0.grid(row = 2, column = 3)
        
        button_2_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(2, 'up'))
        button_2_1 ['font'] = myFont_w
        button_2_1.grid(row = 2, column = 4)
        
        label_endday = tk.Label(Window, text="End Day:", height=2, width=14)
        label_endday['font'] = myFont_w
        label_endday.grid(row=3, column=1)
        
        self.end_day = ttk.Combobox(Window, height=9, width=14)
        self.end_day['font'] = myFont_w
        self.end_day.grid(row=3, column=2)    
        
        self.change_enddays()
        self.end_day.current(int(time.strftime("%d"))-2)
        
        button_3_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(3, 'down'))
        button_3_0 ['font'] = myFont_w
        button_3_0.grid(row = 3, column = 3)
        
        button_3_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(3, 'up'))
        button_3_1 ['font'] = myFont_w
        button_3_1.grid(row = 3, column = 4)
        
        # set up the hour
        label_time = tk.Label(Window, text="Hour:", height = 2, width = 14)
        label_time['font'] = myFont_w
        label_time.grid(row=4, column=1)
            
        self.hour = ttk.Combobox(Window, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], height = 9, width=14)
        self.hour['font'] = myFont_w
        self.hour.grid(row=4, column=2)
        self.hour.current(int(time.strftime("%I"))-1)
        
        button_4_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(4, 'down'))
        button_4_0 ['font'] = myFont_w
        button_4_0.grid(row = 4, column = 3)
        
        button_4_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(4, 'up'))
        button_4_1 ['font'] = myFont_w
        button_4_1.grid(row = 4, column = 4)
        
        label_minute = tk.Label(Window, text="Minute:", height=2, width=14)
        label_minute['font'] = myFont_w
        label_minute.grid(row=5, column=1)
        
        debugTime = str(int(time.strftime("%M"))+1)
        if len(debugTime) == 1:
            debugTime = '0' + debugTime 

        self.minute = ttk.Combobox(Window, values=["00", "15", "30", "45", debugTime], height=9, width=14)
        self.minute['font'] = myFont_w
        self.minute.grid(row=5, column=2)
        self.minute.current(0)
        
        button_5_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(5, 'down'))
        button_5_0 ['font'] = myFont_w
        button_5_0.grid(row = 5, column = 3)
        
        button_5_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(5, 'up'))
        button_5_1 ['font'] = myFont_w
        button_5_1.grid(row = 5, column = 4)
        
        
        label_am_pm = tk.Label(Window, text ="AM/PM:", height=2, width=14)
        label_am_pm['font'] = myFont_w
        label_am_pm.grid(row=6, column=1)
        
        self.am_pm = ttk.Combobox(Window, values=["AM", "PM"], height=9, width=14)
        self.am_pm['font'] = myFont_w
        self.am_pm.grid(row=6, column=2)
        self.am_pm.current(0)
        
        button_6_0 = tk.Button(Window, text="AM", height = 2, width = 10, command=lambda: self.arrowButtons(6, 'down'))
        button_6_0 ['font'] = myFont_w
        button_6_0.grid(row = 6, column = 3)
        
        button_6_1 = tk.Button(Window, text="PM", height = 2, width = 10, command=lambda: self.arrowButtons(6, 'up'))
        button_6_1 ['font'] = myFont_w
        button_6_1.grid(row = 6, column = 4)
        
        label_repeat = tk.Label(Window, text="Time Interval", height=2, width=14)
        label_repeat['font'] = myFont_w
        label_repeat.grid(row=7, column=1)
        
        self.repeat = ttk.Combobox(Window, values=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], height=9, width=14)
        self.repeat['font'] = myFont_w
        self.repeat.grid(row=7, column=2)
        self.repeat.current(0)
        
        button_7_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(7, 'down'))
        button_7_0 ['font'] = myFont_w
        button_7_0.grid(row = 7, column = 3)
        
        button_7_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(7, 'up'))
        button_7_1 ['font'] = myFont_w
        button_7_1.grid(row = 7, column = 4)

        label_number = tk.Label(Window, text="Number of pills", height=2, width=14)
        label_number['font'] = myFont_w
        label_number.grid(row=8, column=1)
        
        self.pills = ttk.Combobox(Window, values=["1", "2", "3", "4", "5"], height=9, width=14)
        self.pills['font'] = myFont_w
        self.pills.grid(row=8, column=2)
        self.pills.current(0)
        
        button_8_0 = tk.Button(Window, text="DOWN", height = 2, width = 10, command=lambda: self.arrowButtons(8, 'down'))
        button_8_0 ['font'] = myFont_w
        button_8_0.grid(row = 8, column = 3)
        
        button_8_1 = tk.Button(Window, text="UP", height = 2, width = 10, command=lambda: self.arrowButtons(8, 'up'))
        button_8_1 ['font'] = myFont_w
        button_8_1.grid(row = 8, column = 4)

        close = tk.Button(Window, text="Back", command=Window.destroy, height=2, width=16)
        close['font'] = myFont_w
        close.grid(row=1, column=0)
        
        
        # once click the confirm button, get values from all combobox to get the scheduled time
        confirm = tk.Button(Window, text="Confirm", command=self.confirm, height=2, width=16)
        confirm['font'] = myFont_w
        confirm.grid(row=2, column=0)
        
        # add the command for clear button to set all values to default values
        clear = tk.Button(Window, text="Clear", command=self.clear_time, height=2, width=16)
        clear['font'] = myFont_w
        clear.grid(row=3, column=0)
        
        self.confirm_time_start = tk.Label(Window, text="", height=2, width=16)
        self.confirm_time_start['font'] = myFont_w
        self.confirm_time_start.grid(row=4, column=0)
        
        self.confirm_time_end = tk.Label(Window, text="", height=2, width=16)
        self.confirm_time_end['font'] = myFont_w
        self.confirm_time_end.grid(row=5, column=0)
        
    def confirm(self):
        self.confirm_time_start.config(text="Start:" + self.start_month.get() + "," + self.start_day.get() + "," + self.hour.get() + ":" + self.minute.get() + "," + self.am_pm.get())
        self.confirm_time_end.config(text="End:" + self.end_month.get() + "," + self.end_day.get() + "," + self.hour.get() + ":" + self.minute.get() + "," + self.am_pm.get())

        timeAdjusted = int(self.hour.get())
        if self.am_pm.get() == 'PM':
            if timeAdjusted != 12:
                timeAdjusted += 12;

        elif self.am_pm.get() == 'AM' and timeAdjusted == 12:
            timeAdjusted = 0

        if monthDict[self.start_month.get()] < int(time.strftime("%m")):
            start_year = int(time.strftime("%Y"))+1
        else:
            start_year = int(time.strftime("%Y"))

        newItem = dispenseItem(uuid.uuid4().hex, start_year, int(monthDict[self.start_month.get()]), int(self.start_day.get()), (str(timeAdjusted) + ":" + self.minute.get()), False, int(self.pills.get()))
        self.dispenseEvents.append(newItem)
        self.queue.put('update')
        print("Confirmed Event: " + "Start day:" + self.start_month.get() + ", " + self.start_day.get() + ", " + self.hour.get() + ":" + self.minute.get() + ", " + self.am_pm.get() + "   End day:" + self.end_month.get() + ", " + self.end_day.get() + ", " + self.hour.get() + ":" + self.minute.get() + ", " + self.am_pm.get())
            
        self.dispenseWindow()

    def clear_time(self):
        self.confirm_time_start.config(text="")
        self.confirm_time_end.config(text="")
        # remove the time string from the database

    def change_startdays(self):
        # different number of days of months
        if( (self.start_month.get()=="Jan") or (self.start_month.get()=="Mar") or (self.start_month.get()=="May") or (self.start_month.get()=="July") or (self.start_month.get()=="Aug") or (self.start_month.get()=="Oct") or (self.start_month.get()=="Dec") ):
            s_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
        elif(self.start_month.get()=="Feb"):
            s_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
        elif((self.start_month.get()=="Apr") or (self.start_month.get()=="June") or (self.start_month.get()=="Sep") or (self.start_month.get()=="Nov")):
            s_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
            
        self.start_day.config(values=s_days)
        self.start_day.after(200, self.change_startdays)

    def change_enddays(self):
        # different number of days of months
        if( (self.end_month.get()=="Jan") or (self.end_month.get()=="Mar") or (self.end_month.get()=="May") or (self.end_month.get()=="July") or (self.end_month.get()=="Aug") or (self.end_month.get()=="Oct") or (self.end_month.get()=="Dec") ):
            e_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
        elif(self.end_month.get()=="Feb"):
            e_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
        elif((self.end_month.get()=="Apr") or (self.end_month.get()=="June") or (self.end_month.get()=="Sep") or (self.end_month.get()=="Nov")):
            e_days=["1", "2", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
            
        self.end_day.config(values=e_days)
        self.end_day.after(200, self.change_enddays)

    def __init__(self, ws, queue, endCommand, dispEvents, clearEvents):

        myFont_main = font.Font(size=16)
        
        
        # Object to keep track of dispensing events.
        self.dispenseEvents = dispEvents

        self._is_running = True
        self.queue = queue
        # Set up the GUI
        ws.geometry("800x480")
        ws.attributes("-fullscreen", True)      
        
        
        # current clock display
        self.clock_disp = tk.Label(ws, text="", font=("Helvetica", 50), fg="white", bg="black")
        self.clock_disp.grid(row=0, column=0)

        # show the exact date
        self.clock_disp1 = tk.Label(ws, text="", font=("Helvetica", 35), fg="white", bg="black")
        self.clock_disp1.grid(row=1, column=0)        
        self.clock()

        space = tk.Label(ws, text=" ")
        space.grid(row=2, column=0)

        # upcoming events display
        notice = tk.Label(ws, text="Upcoming Events", font=("Helvetica", 24))
        notice.grid(row=3, column=0)

        self.events = tk.Listbox(ws, height = 9, width = 40, activestyle = 'none', font=("Helvetica", 18))
        self.events.grid(row=4, column=0)


        button_clear = tk.Button(ws, text="Clear events", font=("Helvetica", 19), command=lambda:clearEvents(), bg='White', fg='Black', height=2, width=10)
        button_clear.grid(row=0, column=1)


        # schedule button jump to the schdule page
        button = tk.Button(ws, text="Schedule", bg='White', fg='Black', font=("Helvetica", 19), height = 2, width = 10, command=lambda:self.scheduleWindow())

        button.grid(row=1, column=1)

        close_main = tk.Button(ws, text="Close", command=endCommand, bg='White', fg='Black', font=("Helvetica", 19), height=2, width=10)
        close_main.grid(row=2, column=1)

        next_notice = tk.Label(ws, text="Next Event", font=("Helvetica", 24))
        next_notice.grid(row=3, column=1)
        
        self.next_event = tk.Listbox(ws, height = 9, width = 38, activestyle = 'none', font=("Helvetica", 18))
        self.next_event.grid(row=4, column=1)
        
    def processIncoming(self, clearEvents):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                if msg == 'update':
                    print("----processing----")
                    print(self.dispenseEvents)
                    self.events.delete(0, self.events.size())

                    #Update database
                    updateDatabase('data.txt', self.dispenseEvents)

                    # Iterate though events
                    for item in self.dispenseEvents:
                        # Adjust time to AM/PM
                        dispTime = int(item.dispenseTime.split(':')[0])
                        if dispTime < 12 or dispTime == 24:
                            ampm = "AM"
                        else:
                            ampm = "PM"
                            dispTime = dispTime - 12
                        if dispTime == 0:
                            dispTime = 12
                        dispTime = str(dispTime) + ':' + item.dispenseTime.split(':')[1] + ampm

                        # Add to event board
                        if item.google_cal:
                            listString = "Date:" + months[item.start_month-1] + " " + str(item.start_day) + ", at " + dispTime + ";  From Google"
                        else:
                            listString = "Date:" + months[item.start_month-1] + " " + str(item.start_day) + ", at " + dispTime
                        self.events.insert(END,"DispTime: " + listString)

                elif msg == 'dispensing':
                    print("dispensing")
                elif msg == 'dispenseError':
                    print("dispensing ERROR")

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
        global currentlyDispensing
        GPIO.output(enable_pin,0)

        # Create the queue
        self.queue = queue.Queue(  )

        # Create the main calendar object from the database
        print('Reading DB')
        try:
            self.dispenseEvents = readDatabase('data.txt')
        except Exception as inst:
            print("Error reading database!")
            self.dispenseEvents = []
        print('DB read!')

        # Bracelet Thread


        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication, self.dispenseEvents, self.clearEvents)

        # Google Calendar Setup
        # Adapted from the Google Calendar API example provided by Google.
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_console()
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

        # Set up the threads to do asynchronous I/O
        self.running = 1
        self.dispenseThread = threading.Thread(target=self.dispenseCheckWorkerThread)
        self.calendarThread = threading.Thread(target=self.calendarWorkerThread)
        self.braceletThread = threading.Thread(target=self.braceletWorkerThread)
        self.dispenseThread.start()
        self.calendarThread.start()
        self.braceletThread.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )

    def clearEvents(self, modifier = 'all', removedEvent = []):
        if modifier == 'all':
            self.dispenseEvents.clear()
        elif modifier == 'item':
            if removedEvent:
                self.dispenseEvents.remove(removedEvent)
        print("------------EVENTS CLEARED------------------")
        self.queue.put('update')

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(self.clearEvents)
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            print("GUI dying!")
            self.master.destroy()
        self.master.after(200, self.periodicCall)

    def dispenseCheckWorkerThread(self):
        """
        This thread continuously comapres the current time to 
        the time inside every dispenseItem inside DispenseEvents,
        and if it matches, we send the dispense signal into the queue.
        """
        
        global currentItem
        global currentlyDispensing
        global dispenseTimer
        global dispensedPills
        while self.running:
            print('Checking dispense time')
            currentTime = str(int(time.strftime("%H"))) + ":" + time.strftime("%M")
            for item in self.dispenseEvents:
                if not currentlyDispensing and int(time.strftime("%d")) >= item.start_day and int(time.strftime("%m")) >= item.start_month:
                    if currentTime == item.dispenseTime:
                        currentItem = item
                        currentlyDispensing = True
                        self.queue.put('dispensing')
                        print('Dispense command sent')
                        break

            if not currentlyDispensing:
                print('Checking dispense time')
                time.sleep(5)
            if currentlyDispensing:
                if dispenseTimer == 0:

                    self.clearEvents('item', currentItem)
                    self.queue.put('update')
                    GPIO.output(enable_pin,1)
                    GPIO.output(buzzer_pin,1)
                    dispense(3/1000.0,128)
                    print('rotation')

                time.sleep(0.2)
                dispenseTimer = dispenseTimer + 1

                if dispenseTimer > 20:
                    print('checks')
                    dispensedPills = dispensedPills + 1
                    dispenseTimer = 0
                    GPIO.output(buzzer_pin,0)
                    if not GPIO.input(tripwire_input_pin):
                        print('laser')
                        self.queue.put('dispenseError')
                        dispensedPills = 0
                        dispenseTimer == 0
                        currentlyDispensing = False
                    else:
                        #Remove used dispenseItem
                        dispensedPills = 0
                        print('success')
                        self.queue.put('dispenseSuccess')
                        currentlyDispensing = False

                    currentlyDispensing = False
                    GPIO.output(enable_pin,0)
                    time.sleep(0.1)
                     # if currentlyDispensing and chamber_led_input_pin:
                     #     print('chamber')
                    #     self.queue.put('dispenseError')
                    #     dispensedPills = 0
                    #     dispenseTimer == 0
                    #     currentlyDispensing = False

                    # else:
                    #     #Remove used dispenseItem
                    #     dispensedPills = 0
                    #     self.queue.put('dispenseSuccess')
                    #     currentlyDispensing = False

        print("dispenseCheck worker dying")

    def calendarWorkerThread(self):
        """
        Handles all async Google Calendar functionality.
        """
        print("Started Calendar Thread")
        while self.running:

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=5, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                time.sleep(3)

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                if 'PILL' in event['summary']:

                    # Check for duplicates
                    if self.dispenseEvents:
                        duplicate = False
                        for item in self.dispenseEvents:
                            if item.cal_id == event['id']:
                                duplicate = True

                        if not duplicate:
                            parts = event['start'].get('dateTime').split('T')
                            dateParts = parts[0].split('-')
                            dispenseTimeParts = parts[1].split(':')
                            dispenseTime = str(int(dispenseTimeParts[0])) + ":" + dispenseTimeParts[1]

                            newItem = dispenseItem(event['id'],int(dateParts[0]), int(dateParts[1]), int(dateParts[2]), dispenseTime, True)
                            self.dispenseEvents.append(newItem)
                            self.queue.put('update')
                    else:
                        parts = event['start'].get('dateTime').split('T')
                        dateParts = parts[0].split('-')
                        dispenseTimeParts = parts[1].split(':')
                        dispenseTime = str(int(dispenseTimeParts[0])) + ":" + dispenseTimeParts[1]
                        newItem = dispenseItem(event['id'],int(dateParts[0]), int(dateParts[1]), int(dateParts[2]), dispenseTime, True)
                        self.dispenseEvents.append(newItem)
                        self.queue.put('update')

        # GUI thread shutting down
        print("calendar worker dying")

    def braceletWorkerThread(self):
        """
        This worker thread handles he connection with the bracelet device,
        and sends all necessary dispensing data.
        """

        global currentlyDispensing
        
        while self.running:
            try:
                print("Connecting...")
                dev = btle.Peripheral("1c:9d:c2:82:9e:1a") # board1new

                print("Services...")
                for svc in dev.services:
                    print(str(svc))

                bracelet = btle.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
                service = dev.getServiceByUUID(bracelet)

                chtruuid = btle.UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")
                chtr = service.getCharacteristics(chtruuid)[0]
                print(str(chtr.read()))
                
                while self.running:
                    if currentlyDispensing:
                        chtr.write(str.encode("dispensing"))
                        time.sleep(5)
                        chtr.write(str.encode("normal"))

                # time.sleep(0.1)
            except Exception:
                print('Error connecting')

        print("braceletworker dying")   

    def endApplication(self):
        print("end command sent")
        self.running = 0

#############################################
#     Main
#############################################

print("Starting Main Program")
ws = tk.Tk()
ws.title("Home Page")

currentlyDispensing = False
client = ThreadedClient(ws)

print("starting loop")
ws.mainloop()
print("loop done")

client.endApplication()
print("threads alive: " + str(client.dispenseThread.is_alive()))
GPIO.cleanup()
sys.exit(1)


