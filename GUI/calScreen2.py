# Import Required Library
from tkinter import *
import time

root = Tk(  )

# Set geometry
root.geometry("800x480")
#root.attributes("-fullscreen", True)

# background_image = PhotoImage(file = "/home/pi/Pill-Dispenser-ECE591/GUI/images/sea_lowres.png")
# background_label = Label(root, image=background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

# myCanvas = Canvas(root, bg="white", height=100, width=100)
# myCanvas.pack()

# myCanvas.create_rectangle(1*100, 1*100, 2*100, 2*100, fill='grey', outline='black')
# myCanvas.pack()
# myCanvas.create_rectangle(2*100, 2*100, 3*100, 3*100, fill='grey', outline='black')
# myCanvas.create_rectangle(0*100, 5*100, 1*100, 6*100, fill='grey', outline='black')

# for r in range(6):
#    for c in range(3):
#    		myCanvas.create_rectangle((c-1)*100, (r-1)*100, c*100, r*100, fill='grey', outline='black')
#    		myCanvas.pack()

board_canvas = Canvas(root, borderwidth=1)
board_canvas.grid(row=1, column=0, sticky='ew', columnspan=8, rowspan=8)

x = 100
y = 100

board_canvas.create_rectangle(0, 0, x, y, fill='black')
board_canvas.create_rectangle(100, 0, 200, y, fill='white')
board_canvas.create_rectangle(200, 0, 300, y, fill='black')


root.mainloop(  )


