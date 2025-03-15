# 5-rgb on of and setting color using microdot and script
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

# Initialize the Microdot web server
app = Microdot()
Response.default_content_type = "application/json"

# HTML Web Page with Buttons and RGB Input
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32-S3 RGB Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .button { padding: 15px 30px; font-size: 20px; cursor: pointer; margin: 10px; }
        input { width: 50px; text-align: center; font-size: 16px; }
    </style>
    <script>
        

        function setColor() {
            let r = document.getElementById("r").value || 0;
            let g = document.getElementById("g").value || 0;
            let b = document.getElementById("b").value || 0;
            
            fetch(`/set_color?r=${r}&g=${g}&b=${b}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').innerText = "RGB LED set to " + data.status;
                });
        }
    </script>
</head>
<body>
    <h1>ESP32-S3 RGB LED Control</h1>
    <p id="status">RGB LED </p>
    

    <h3>Set Custom RGB Color</h3>
    <input type="number" id="r" min="0" max="255" placeholder="R">
    <input type="number" id="g" min="0" max="255" placeholder="G">
    <input type="number" id="b" min="0" max="255" placeholder="B">
    <button class="button" onclick="setColor()">Set Color</button>
</body>
</html>
"""

# Serve the Web Page
@app.route("/")
def index(request):
    response = Response(body=HTML_PAGE)
    response.headers["Content-Type"] = "text/html"
    return response

# API to Turn ON RGB LED (Set to White)
@app.route("/on", methods=["POST"])
def turn_on(request):
    print("Turning ON RGB LED")
    set_rgb(255, 255, 255)  # White color
    return {"status": "ON"}

# API to Turn OFF RGB LED (Set to Black)
@app.route("/off", methods=["POST"])
def turn_off(request):
    print("Turning OFF RGB LED")
    set_rgb(0, 0, 0)  # Turn off
    return {"status": "OFF"}

# API to Set Custom RGB Color
@app.route("/set_color", methods=["POST"])
def set_color(request):
    try:
        print("Received request:", request.args)
        r = int(request.args.get('r', 0))
        g = int(request.args.get('g', 0))
        b = int(request.args.get('b', 0))
        
        # Validate RGB values (0-255)
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB values must be between 0 and 255")
        
        print(f"Setting color: R={r}, G={g}, B={b}")
        set_rgb(r, g, b)
        return {"status": f"R:{r}, G:{g}, B:{b}"}
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}

# Start the Microdot Web Server
print("Starting server...")
app.run(host="0.0.0.0", port=80)