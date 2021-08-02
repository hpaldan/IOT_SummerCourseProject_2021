#from mqtt import MQTTClient
from mqtt import MQTTClient_lib as MQTTClient
from network import WLAN
import machine
import time
import math
import config

adc = machine.ADC()
apin = adc.channel(pin='P19')


Q = b'0'

def sub_cb(topic, msg):
    global Q
    Q = msg

wlan = WLAN(mode=WLAN.STA)
wlan.connect(config.WIFI_NAME, auth=(WLAN.WPA2, config.WIFI_PW), timeout=5000)

while not wlan.isconnected():  
    machine.idle()

print("Connected to WiFi\n")

client = MQTTClient(config.PYCOM_NAME, config.SERVER_NAME,user=config.ADA_USERNAME, password= config.AIO_KEY, port=1883)

client.set_callback(sub_cb)
client.connect()
client.subscribe(topic=config.TOPIC_NAME)
print('Subscription established\n')

k = 0
interval = 50

while True:
    
    sinVal = 5*math.sin(2*math.pi*k/interval)
    print('Sinval is:' +str(sinVal))
    k = k+1
    if k == interval:
        k = 0
    client.publish(topic=config.TOPIC_NAME, msg=str(sinVal))
    
    time.sleep(5)
    client.check_msg()
    Q = float(Q)
    Q1 = round(Q,2)
    print(Q1)
    Q2 = float("{0:.2f}".format(Q))
    print(Q2)    


    