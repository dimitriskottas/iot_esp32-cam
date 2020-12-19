import uos
import machine 
import ntptime
import time
import camera

from umqtt.simple2 import MQTTClient

wait_ms = 5000 #Sec between photos

#MQTT Configurations
mqtt_server = '192.168.*.*'
mqtt_client_id = 'esp32-camera'
mqtt_topic = b'Camera/Images'
mqtt_user = b'***'
mqtt_pass = b'***'

try:
    # camera init
    led = machine.Pin(4, machine.Pin.OUT) #Pin for LED

    camera.init(0, format=camera.JPEG)  # ESP32-CAM
    
    c = MQTTClient(mqtt_client_id, mqtt_server, user = mqtt_user, password = mqtt_pass)
    c.connect()

    # ntp sync for date
    ntptime.settime()
    rtc = machine.RTC()

except Exception as e:
    print("Error ocurred: " + str(e))
    time.sleep_ms(5000)
    machine.reset()

#error_counter = 0
while True:
    try:
        # prepare for photo
        led.value(1)
        led.value(0)

        # take photo
        buf = camera.capture()
        # save photo
        timestamp = rtc.datetime()
        time_str = '%4d%02d%02d%02d%02d%02d' %(timestamp[0], timestamp[1], timestamp[2], timestamp[4], timestamp[5], timestamp[6])

        c.publish(mqtt_topic, buf)

        # sleep
        time.sleep_ms(wait_ms)