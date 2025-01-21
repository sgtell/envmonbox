#!/home/tell/venv/bin/python3
#
# based on pitft code 
# 	SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# 	SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-

import time
import subprocess
import digitalio
import board
import os
import re
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
from perlish import *


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp_width = 135

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=disp_width,
    height=240,
    x_offset=53,
    y_offset=40,
)

def get_ip():
    cmd = "hostname -I";
    ipstr = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return ipstr.rstrip("\r\n")

def get_time():
    tmnow = time.localtime()
    return sprintf("%02d:%02d", tmnow.tm_hour, tmnow.tm_min);

def get_cpu_load():
    #top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    cmd = "uptime"
    upstr = subprocess.check_output(cmd, shell=True).decode("utf-8")
    m = re.search(r"load average:\s+([0-9.]+)", upstr)
    if(m):
        cpu = float(m.group(1))
        return cpu
    else:
        printf("get_cpu_load fail \"%s\"\n", upstr)
        return 0.0

def get_cpu_temp():
    fn = "/sys/class/thermal/thermal_zone0/temp"
    f = open(fn, "r");
    s = f.readline(); # .decode("utf-8")
    f.close()
    rawtemp = float(s)
    return rawtemp/1000.0

def get_temp_hum():
    cmd = "sensors shtc1-i2c-1-70"
    f = os.popen(cmd, "r");
    temp = None
    hum = None
    for line in f:
        #printf("th_line: %s\n", line.rstrip("\r\n"))
        m = re.match(r"temp1:\s*([+0-9.]+)", line)
        if(m):
            temp = float(m.group(1))
        m = re.match(r"humidity1:\s*([+0-9.]+)", line)
        if(m):
            hum = float(m.group(1))
    f.close()
    return (temp, hum)


# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # # Shell scripts for system monitoring from here:
    # # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    # cmd = "hostname -I | cut -d' ' -f1"
    # IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    # CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    # MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    # Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long

    #Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    IP = get_ip()
    cpuload = get_cpu_load()
    cputemp = get_cpu_temp()
    cpustr = sprintf("CPU t=%2.1f L=%.1f", cputemp, cpuload)
    timestr = get_time()
    (temp, hum) = get_temp_hum()
    tempf = temp * 1.8 + 32
    thstr   = sprintf("room    %2.0fF  %2.0f%% H", tempf, hum)
#    outtstr = sprintf("outside %2.0fF\n", outtempf);
    outtstr = sprintf("outside ___\n");
    
    # Write four lines of text.
    y = top
    bbox = font.getbbox(timestr)
    w = bbox[2] - bbox[0]
#    printf("timestr bbox=%s %s w=%d\n", str(bbox), timestr, w);
    draw.text((disp_width - w + 75, y), timestr, font=font, fill="#FFFFFF")
    s = bbox[1] + bbox[3];
    y += s

    #    m = font.getmetrics()
    draw.text((x, y), IP, font=font, fill="#FF8000")
    y+= s
#    y += font.getmetrics(IP)[1]
#    font.getmetrics()[1]
#    draw.text((x, y), CPU, font=font, fill="#FFFF00")
#    y += s
#    y += font.getmetrics(CPU)[1]
#    draw.text((x, y), MemUsage, font=font, fill="#00FF00")
#    y += s
#    y += font.getmetrics(MemUsage)[1]
#    draw.text((x, y), Disk, font=font, fill="#0000FF")
#    y += s
#    y += font.getmetrics(Disk)[1]
    draw.text((x, y), cpustr, font=font, fill="#008F8F")
    y += s
    y += 2
    draw.text((x, y), thstr, font=font, fill="#FFFFFF")
    y += s
    draw.text((x, y), outtstr, font=font, fill="#FFFFFF")
    y += s

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.3)