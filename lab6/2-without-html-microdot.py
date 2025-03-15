# 2-rgb on off  using microdot without html code
from microdot import Microdot, Response
from machine import Pin
from neopixel import NeoPixel
import network
import utime as time



# WiFi Credentials
WIFI_SSID = 'Ibrahim(4G)'
WIFI_PASS = '47224723'


print(f"Connecting to WiFi network '{WIFI_SSID}'...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)


wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    time.sleep(1)
    print('WiFi connect retry ...')

print('WiFi Connected!')
print('WiFi IP:', wifi.ifconfig()[0])

# Static IP Configuration
STATIC_IP = "192.168.1.60"  # Change this IP if needed
SUBNET_MASK = "255.255.255.0"
GATEWAY = "192.168.1.254"
DNS_SERVER = "8.8.8.8"  # Google DNS

# Set Static IP
wifi.ifconfig((STATIC_IP, SUBNET_MASK, GATEWAY, DNS_SERVER))



# Define the pin connected to the NeoPixel
pin = Pin(48, Pin.OUT)
np = NeoPixel(pin, 1)  # 1 NeoPixel

# Function to set RGB color
def set_rgb(r, g, b):
    np[0] = (r, g, b)  # Set the color for the first NeoPixel
    np.write()  # Write the color to the NeoPixel

app = Microdot()
# Initialize the Microdot web server
@app.route('/')
def index(request):
    return 'Hello, World!'

@app.route('/rgb/<state>')
def led_control(request, state):
    if state == 'on':
        # Turn on LED (assuming it's connected to GPIO 2)
        set_rgb(255,0,0)
        return 'RGB LED turned ON'
    elif state == 'off':
        # Turn off LED
        set_rgb(0,0,0)
        return 'RGB LED turned OFF'
    else:
        return 'Invalid state'


# Start the Microdot Web Server
print("Starting server...")
#app.run(host="0.0.0.0", port=80)
app.run(port=80)
