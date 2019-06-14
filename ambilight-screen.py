from PIL import Image, ImageGrab
import json
import time
import colorsys
import requests

# Program start information
print('\033[95m\033[1m--- OpenHAB Ambilight Screen v0.1.0 ---\033[0m\n\033[94m\033[1m[' +
      time.strftime('%H:%M:%S') +
      '] Started program.\033[0m')

# Loop
try:
    while True:
        try:
            # Load JSON data
            with open('config.json') as json_file:
                json_data = json.load(json_file)
                while True:
                    # Get average color from main screen
                    avg_color = ImageGrab.grab().resize((1, 1), Image.ANTIALIAS).getpixel((0, 0))

                    # Convert RGB to HSV
                    h, s, v = colorsys.rgb_to_hsv((avg_color[0]/255.0), (avg_color[1]/255.0), (avg_color[2]/255.0))
                    color_data = (str(h*360.0)+','+str(s*100.0)+','+str(v*100.0))

                    # Send HSV color to openHAB server
                    r = requests.post(json_data['openhab_url']+'/rest/items/'+json_data['openhab_item_name'],
                                      data=color_data,
                                      auth=(json_data['openhab_username'], json_data['openhab_password']))
                    
                    # Page not found error
                    if r.status_code == 404:
                        print('\033[91m\033[1m['+time.strftime('%H:%M:%S') +
                              '] Page not found error. ' +
                              'Check URL and item name in config file.\033[0m')
                        time.sleep(1)
                        break

                    # Server authentication error
                    if r.status_code == 401:
                        print('\033[91m\033[1m['+time.strftime('%H:%M:%S') +
                              '] Server authentication error. ' +
                              'Check username and password in config file.\033[0m')
                        time.sleep(1)
                        break
        # Server SSL error
        except requests.exceptions.SSLError:
            print('\033[91m\033[1m['+time.strftime('%H:%M:%S') +
                  '] Server SSL error. Check server SSL certificate.\033[0m')
            time.sleep(1)
            continue

        # Server connection error
        except requests.exceptions.ConnectionError:
            print('\033[91m\033[1m['+time.strftime('%H:%M:%S') +
                  '] Server connection error. Check your internet connection or URL in config file.\033[0m')
            time.sleep(1)
            continue

# JSON file not found error
except FileNotFoundError:
    print('\033[91m\033[1m['+time.strftime('%H:%M:%S') +
          '] No config.json file! Create it using config.json.sample as example.' +
          'More informations in README file.\033[0m\n\033[94m\033[1m[' +
          time.strftime('%H:%M:%S') +
          '] Stopped program.\033[0m')

# JSON data not completely error
except KeyError:
    print('\033[91m\033[1m['+time.strftime('%H:%M:%S') +
          '] Data in config.json file isn\'t completely. Correct them.\033[0m\n\033[94m\033[1m[' +
          time.strftime('%H:%M:%S') +
          '] Stopped program.\033[0m')

# JSON broken structure error
except json.decoder.JSONDecodeError:
    print('\033[91m\033[1m[' +
          time.strftime('%H:%M:%S') +
          '] Structure of config.json file is broken. Correct it.\033[0m\n\033[94m\033[1m[' +
          time.strftime('%H:%M:%S') +
          '] Stopped program.\033[0m')

# Program stop information
except KeyboardInterrupt:
    print('\033[94m\033[1m[' +
          time.strftime('%H:%M:%S') +
          '] Stopped program.\033[0m')
