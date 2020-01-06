from tkinter import *

import serial
import sys

# Graphic interface for the send program
master = Tk()
scales=list()
Nscales=60

for i in range(Nscales):
    w=Scale(master, from_=9, to=0) # creates widget
    w.grid(row=i//10,column=i-(i//10)*10)
    scales.append(w) # stores widget in scales list

# send serial message 
# Don't forget to establish the right serial port ******** ATTENTION
#SERIALPORT = "/dev/ttyS3"
SERIALPORT = "/dev/tty.usbserial-DA00FU88"
BAUDRATE = 115200
ser = serial.Serial()
try:
    ser.open()
except serial.SerialException:
    print("Serial {} port not available".format(SERIALPORT))
    exit()

def sendUARTMessage(msg):
    ser.write(msg.encode())
    print("Message pute <" + msg + "> sent to micro-controller." )


def read_scales():
    b['state'] = 'disabled'
    for i in range(Nscales):
        column = i-(i//10)*10
        row = i//10
        if (scales[i].get()>0) :
                print("Fire x=%d, y=%d has value %d" %( row, column, scales[i].get()) )
        sendUARTMessage("(%d,%d,%d)" %(row, column, scales[i].get()))
    
    b['state'] = 'normal'

b=Button(master,text="Send Values",highlightcolor="blue",command=read_scales, state="disabled") # button to read values
serialButton=Button(master,text="Open Serial",highlightcolor="blue",command=initUART) # button to read values
b.grid(row=6,column=7,columnspan = 3)
serialButton.grid(row=6, column=0, columnspan = 3)

# initUART()

mainloop()