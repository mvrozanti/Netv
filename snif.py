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

def on_close():
    # if we’re using Windows, turn off promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

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
pixels = []
x, y = 0, 0
def draw():
    bs = sniffer.recvfrom(65565)
    les_bytes = bs[0]
    rgb = []
    global pixels
    global x
    global y
    for i in range(len(les_bytes)):
        rgb.append(les_bytes[i] % 255)
        if len(rgb) == 3:
            color = tuple_to_color(tuple(rgb))
            rgb.clear()
            pixel = c.create_line((x+3, y+3), (x+4, y+4), fill=color, width=10)
            if len(pixels) <= x:
                pixels.insert(x, [])
            pixels[x].insert(y+1, pixel)
            #y+=1
            #if y > HEIGHT:
            #    y = 0
            #    x += 1
            #    if x > WIDTH:
            #        x = y = 0
            # shift *
            for row in pixels:
                for p in row:
                    xy = c.coords(p)
                    p_width = float(c.itemcget(p, 'width'))
                    xy[1] = xy[1] + p_width#y++
                    xy[3] = xy[3] + p_width
                    if xy[1] > HEIGHT:
                        xy[1] = 0#y=0
                        xy[3] = 1
                        xy[0] = xy[0] + p_width#x++
                        xy[2] = xy[2] + p_width
                    if xy[0] > WIDTH:
                        xy[0] = 0#x=y=0
                        xy[2] = 1
                        xy[1] = 0
                        xy[3] = 1
                    c.coords(p, xy)
                    c.update_idletasks()
                    c.update()
    c.after(1, draw)
draw()
t.protocol('WM_DELETE_WINDOW', on_close)
t.mainloop()
