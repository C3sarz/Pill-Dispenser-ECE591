# Import Required Library
from tkinter import *
import time
from time import strftime
import datetime

root = Tk(  )
root.title('Calendar')

# Set geometry
root.geometry("800x480")
#root.attributes("-fullscreen", True)

canvas = Canvas(root, borderwidth=1, width=800, height=480)
canvas.pack(expand=YES, fill=BOTH)

for r in range(5):
   for c in range(8):
   		print(c)
   		canvas.create_rectangle((c-1)*100, (r-1)*100, c*100, r*100, fill='grey', outline='black')
# board_canvas = Canvas(root, borderwidth=10)
# board_canvas.grid(row=8, column=0, sticky='ew', columnspan=8, rowspan=8)

# x = 100
# y = 100

# board_canvas.create_rectangle(0, 0, x, y, fill='black')
# board_canvas.create_rectangle(100, 0, 200, y, fill='white')
# board_canvas.create_rectangle(200, 0, 300, y, fill='black')

canvas.pack()
root.mainloop(  )


