#from mqtt import MQTTClient
from mqtt import MQTTClient_lib as MQTTClient
from network import WLAN
import machine
from machine import Pin
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


while True:
    milliVal = apin.voltage()   
    celsius = (milliVal - 500.0) / 10.0 + 62
    
    print('celsius is:' +str(celsius))

    client.publish(topic=config.TOPIC_NAME, msg=str(celsius))
    
    print('going to sleep')
    time.sleep(60*10)
    print('rebooting')
