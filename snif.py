from tkinter import *
import socket
import os
import numpy as np
import winsound
# host to listen on
host = '127.0.0.1'
# create a raw socket and bind it to the public interface
if os.name == 'nt':
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 12))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
# if we’re using Windows, we need to send an IOCTL
# to set up promiscuous mode

WIDTH=600
HEIGHT=600

if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
def tuple_to_color(rgb):
    color = '#'
    r,g,b=rgb[0],rgb[1],rgb[2]
    color+='%02x'%r
    color+='%02x'%g
    color+='%02x'%b
    return color

t = Tk()
c = Canvas(t, width=WIDTH, height=HEIGHT, bg='black')
c.pack()
#img = PhotoImage(width=WIDTH, height=HEIGHT)
#c.create_image((WIDTH/2, HEIGHT/2), image=img, state='normal')
#pixels = []
canvas_columns = []
x, y=1,1
def draw():
    bs = sniffer.recvfrom(65565)
    les_bytes = bs[0]
    rgb = []
    global canvas_columns
    global x
    global y
    for i in range(len(les_bytes)):
        rgb.append(les_bytes[i] % 255)
        if len(rgb) == 3:
            color = tuple_to_color(tuple(rgb))
            col = c.create_line(x, 0, x, HEIGHT, fill=color, width=1)
            canvas_columns.append(col)
            if len(canvas_columns) > WIDTH: 
                c.delete(canvas_columns[0])
                canvas_columns.pop(0)
            # move over shifting * to the right
            for l in canvas_columns:
                xy = c.coords(l)
                xy[0]+=1
                xy[2]+=1
                c.coords(l, xy)
            rgb.clear()       
            c.update_idletasks()
            c.update()
    c.after(1, draw)
draw()
t.mainloop()

# if we’re using Windows, turn off promiscuous mode
if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
