from PIL import Image, ImageGrab
import colorsys, requests, time

while True:
    # Get average color from main screen
    avr_col = ImageGrab.grab().resize((1,1),Image.ANTIALIAS).getpixel((0,0))
    # Convert RGB to HSV
    h,s,v = colorsys.rgb_to_hsv((avr_col[0]/255.0),(avr_col[1]/255.0),(avr_col[2]/255.0))
    dat = (str((int)(h*360.0))+','+str((int)(s*100.0))+','+str((int)(v*100.0)))
    print(dat)
    r = requests.post("", data=dat, auth=('', ''))
    time.sleep(0.4)
