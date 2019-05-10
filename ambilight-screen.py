from PIL import ImageGrab
import time
import os
import colorsys
from colour import Color
import requests
from requests.auth import HTTPBasicAuth
LOOP_INTERVAL  = 0.4
DECIMATE       = 10
while True:
    red = 0
    green = 0
    blue = 0
    #time.sleep(LOOP_INTERVAL)
    image = ImageGrab.grab()
    for y in range(0, image.size[1], DECIMATE):
        for x in range(0, image.size[0], DECIMATE):
            color = image.getpixel((x, y))
            red = red + color[0]
            green = green + color[1]
            blue = blue + color[2]
    r = (( red / ( (image.size[1]/DECIMATE) * (image.size[0]/DECIMATE) ) ) )/255.0
    g = ((green / ( (image.size[1]/DECIMATE) * (image.size[0]/DECIMATE) ) ) )/255.0
    b = ((blue / ( (image.size[1]/DECIMATE) * (image.size[0]/DECIMATE) ) ) )/255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (int)(h*360.0)
    l = (int)(l*100.0)
    s = (int)(s*100.0)
    if s < 80:
        s = s + 20
    else:
        s = 100
    dat = (str(h)+','+str(s)+','+str(l))
    print(dat)
    rr = requests.post("https://openhab.serwermsdos.ml/rest/items/ledstrip", data=dat, auth=('', ''))
