import nexmo
import time
import re
import pyperclip
import sys
import requests


url = pyperclip.paste()
nexmokey = 'Enter nexmo key here'  # you can find this here : https://dashboard.nexmo.com/getting-started-guide
nexmosecret = 'Enter nexmo secret here' # you can find this here : https://dashboard.nexmo.com/getting-started-guide
nexmonumber = 'Enter nexmo number here' # you can find this here : https://dashboard.nexmo.com/your-numbers, format is 1xxxxxxxxxx
yournumber = 'Enter your number on which you will receive alert' # in trial version, nexmo allows only the number you used to sign up. format is 1xxxxxxxxxx
client = nexmo.Client(key=nexmokey, secret=nexmosecret)

available = True
r1 = re.compile(',"stock":([0-9]),"')
r2 = re.compile(',"title":"(.*?)",')

while available:
    req = requests.get(url)
    product = r2.findall(req.text)[0]
    l1 = r1.findall(req.text)
    try:
        r3 = int(l1[0])
    except:
        client.send_message({'from' : nexmonumber, 'to' : yournumber, 'text' : 'Check the selly url, may be infinity stock. '})
        sys.exit()
    if int(r3) > 0:
        print(product + ' is in stock on Selly, here is the link: ' + url + ' Quantity: ' + str(r3))
        time.sleep(120)
    else:
        available = False
        while not available:
            req = requests.get(url)
            product = r2.findall(req.text)[0]
            l1 = r1.findall(req.text)
            r3 = int(l1[0])
            if int(r3) > 0:
                client.send_message({'from' : nexmonumber, 'to' : yournumber, 'text' : product + ' is in stock , here is the link: ' + url + ' Quantity: ' + str(r3) + '. '})
                available = True
            else:
                print('Selly product: ' + product + ' is Not available yet.')
                time.sleep(30) # it is set to check every 30 seconds. Change as per your need.
