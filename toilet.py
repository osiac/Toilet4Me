import spidev  
import os  
import math  
import time  
import pigpio  
import math  
import subprocess
import Adafruit_MCP3008
import Adafruit_DHT  
import json  
import RPi.GPIO as GPIO  
import paho.mqtt.publish as publicare  
 
MQTT_HOST = 'mqtt.beia-telemetrie.ro' 
MQTT_TOPIC = 'training/device/TOILET_test' 

spi=spidev.SpiDev()  
spi.open(1,0)   
spi.max_speed_hz=1000000

CLK  = 21
MISO = 19
MOSI = 20
CS   = 23
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 15

while True:
    mq135_adc=mcp.read_adc(0)
    mq137_adc=mcp.read_adc(1)
    mq136_adc=mcp.read_adc(2)
    
    mq135 = (mq135_adc*3.3)/float(4095)  
    mq135 = round(mq135,2)
    
    mq136 = (mq136_adc*3.3)/float(4095)  
    mq136 = round(mq136,2)
    
    mq137 = (mq137_adc*3.3)/float(4095)  
    mq137 = round(mq137,2)
    
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    
    payload_dict={"MQ135":mq135,
                  "MQ136":mq136,
                  "MQ137":mq137,
                  "temperature":round(temperature,2),
                  "humidity":round(humidity,2)}
    print(json.dumps(payload_dict))
    try: 
        publicare.single(MQTT_TOPIC,qos = 1,hostname = MQTT_HOST,payload = json.dumps(payload_dict)) 
    except: 
        pass 
    time.sleep(45)

