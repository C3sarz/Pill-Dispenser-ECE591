# Import Required Library
from tkinter import *
import time
from time import strftime
import datetime

root = Tk(  )
root.title('Clock')

# Set geometry
root.geometry("800x480")
#root.attributes("-fullscreen", True)

canvas = Canvas(root, borderwidth=1, width=800, height=480)
canvas.pack(expand=YES, fill=BOTH)

# Load images
background_image = PhotoImage(file = "/home/pi/Pill-Dispenser-ECE591/GUI/images/beach.png")
bat60 = PhotoImage(file = "/home/pi/Pill-Dispenser-ECE591/GUI/images/bat60.png")
wifi5 = PhotoImage(file = "/home/pi/Pill-Dispenser-ECE591/GUI/images/wifi_d5.png")
wrench_ico = PhotoImage(file = "/home/pi/Pill-Dispenser-ECE591/GUI/images/wrench_plus.png")
speaker_ico = PhotoImage(file = "/home/pi/Pill-Dispenser-ECE591/GUI/images/speaker.png")
 
# This function is used to
# display time on the label
def time():
    string = strftime('%H:%M:%S %p')
    canvas.itemconfigure(lbl, text = string)
    canvas.after(1000, time)
    


 
# Clock and event list
bgr = canvas.create_image(0, 0, image=background_image, anchor=NW)
lbl = canvas.create_text(400, 70, fill = 'black', font = ('Bookman Old Style', 40, 'bold'), stipple='gray25')
title = canvas.create_text(50, 240, fill = 'black', font = ('Arial', 20, 'bold'), stipple='gray25', anchor = W, text="Next items on the calendar:")



#Sidebar code
sidebar = canvas.create_rectangle(750, 0, 800, 480, fill='gray')
wifi_icon = canvas.create_image(776, 26, image=wifi5)
bat_icon = canvas.create_image(777, 80, image=bat60)
settings_icon = canvas.create_image(775, 140, image=wrench_ico)
sound_icon = canvas.create_image(775, 200, image=speaker_ico)
 
# Placing clock at the centre
# of the tkinter window
#lbl.pack(anchor = 'center', pady = 40)
time()
canvas.pack()
 
mainloop()