import threading
import pygame
import random
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

all_bytes = []

if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

def on_close():
    # if we’re using Windows, turn off promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        
def get_latest_packets(sniffer, all_bytes):
    while True:
        bs = sniffer.recvfrom(65565)
        all_bytes.extend(bs[0])
    
t = threading.Thread(target=get_latest_packets, args=(sniffer, all_bytes))
t.daemon = True
t.start()

def tuple_to_color(rgb):
    color = '#'
    r,g,b=rgb[0],rgb[1],rgb[2]
    color+='%02x'%r
    color+='%02x'%g
    color+='%02x'%b
    return color

f = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True
x, y = 0, 0
rgb = []
while True:
    if len(all_bytes) > 0:
        b = all_bytes.pop(0)
        rgb.append(b % 255)
    if len(rgb) == 3:
        x,y = (random.randint(1, WIDTH),random.randint(1, HEIGHT))
        f.set_at((x,y), tuple(rgb))
        rgb.clear()
        pygame.display.flip()
        clock.tick(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
