import network
import utime as time
from microdot import Microdot
import _thread  # Import threading module

# WiFi Credentials
WIFI_SSID = 'Ibrahim(4G)'
WIFI_PASS = '47224723'

# Static IP Configuration
STATIC_IP = "192.168.1.60"
SUBNET_MASK = "255.255.255.0"
GATEWAY = "192.168.1.254"
DNS_SERVER = "8.8.8.8"

# Connect to WiFi
def connect_wifi():
    print(f"Connecting to WiFi network '{WIFI_SSID}'...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.ifconfig((STATIC_IP, SUBNET_MASK, GATEWAY, DNS_SERVER))
    wifi.connect(WIFI_SSID, WIFI_PASS)

    retry = 0
    while not wifi.isconnected():
        retry += 1
        if retry > 10:  # Avoid infinite loop if WiFi fails
            print("Failed to connect to WiFi. Restart ESP32.")
            return False
        time.sleep(1)
        print('WiFi connect retry ...')

    print('Connected! WiFi IP:', wifi.ifconfig()[0])
    return True

# Start Web Server
app = Microdot()

@app.route("/")
def index(request):
    return "Microdot is working on ESP32!"

# Run Microdot in a separate thread
def start_server():
    app.run(port=80)

# Connect WiFi first, then start server
if connect_wifi():
    print("Starting Microdot Web Server...")
    _thread.start_new_thread(start_server, ())
else:
    print("WiFi connection failed. Restart ESP32 and try again.")
