import time
import paho.mqtt.client as mqtt

mqtt_server = '192.168.*.*'
mqtt_topic = b'Camera/Images'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    # generate filename
    timestamp = time.gmtime()
    time_str = time.strptime('%d/%m/%Y %H:%M:%S')
    # Create a file with write byte permission
    f = open('Attendance_Images/'+time_str+'.jpg', "wb")
    f.write(msg.payload)
    f.close()
    print("Image received and saved!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username='***', password='***')
client.connect(mqtt_server, 1883, 60)

client.loop_forever()
