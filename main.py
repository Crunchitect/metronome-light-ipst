from machine import Pin, PWM, ADC, SoftI2C
from time import sleep_ms
from neopixel import NeoPixel
#from ssd1306 import SSD1306_I2C
import network
import usocket as socket
import iLED4
# Function to map a value from one range to another
def map_value(value, from_low, from_high, to_low, to_high):
    scale = (to_high - to_low) / (from_high - from_low)
    mapped_value = to_low + (value - from_low) * scale
    return int(mapped_value)

# Setup OLED display
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
#oled = SSD1306_I2C(128, 64, i2c)

# Setup speaker
spk = PWM(Pin(5,Pin.OUT))
spk.duty(0)

# Setup volume control
vol = ADC(Pin(36))
vol.atten(ADC.ATTN_11DB)

# Setup NeoPixel
np = NeoPixel(Pin(19), 8)

# Setup WiFi
ssid = 'PRESSO_2.4GHz'
password = '0818209828'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
    pass
print('Connection successful')
print(station.ifconfig())

# Function to check Neopixel status and set pic variable accordingly
def check_neopixel():
    if np[0] == (0, 0, 0):  # If Neopixel 0 is off
        pic = "https://png.pngtree.com/png-vector/20190927/ourmid/pngtree-light-bulb-icon-png-image_1749234.jpg"  # Set pic variable to off image URL
    else:
        pic = "https://png.pngtree.com/png-clipart/20230510/original/pngtree-smile-bulb-png-image_9156588.png"  # Set pic variable to on image URL
    return pic

def check_neopixel_2():
    if np[7] == (0, 0, 0):  # If Neopixel 0 is off
        pic2 = "https://png.pngtree.com/png-vector/20190927/ourmid/pngtree-light-bulb-icon-png-image_1749234.jpg"  # Set pic variable to off image URL
    else:
        pic2 = "https://png.pngtree.com/png-clipart/20230510/original/pngtree-smile-bulb-png-image_9156588.png"  # Set pic variable to on image URL
    return pic2

pic = check_neopixel()
pic2 = check_neopixel_2()

# HTML content for the webpage
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/round-slider@1.6.1/dist/roundslider.min.css">

    <script src="https://code.jquery.com/jquery-3.7.1.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/round-slider@1.6.1/dist/roundslider.min.js" ></script>
    <title>Real App 2024 Light Show Metronome real no fake</title>
</head>
<body>
    <h1>METRONOME</h1>
    <div id="slider"></div>    
    <p id="bpm">BPM</p>
</body>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Major+Mono+Display&display=swap');

:root {
    --bpm: 60;
    --hue: calc((180 - var(--bpm) + 33) * 0.8deg);
    --color: hsl(var(--hue) 100% 65%);
    --color-dark: hsl(var(--hue) 100% 40%);
    --color-glow: hsl(var(--hue) 100% 80%);
    --on: 0;
}

* {
    font-family: "Major Mono Display", monospace !important;
}

body {
    background-color: #111;
}

#slider .rs-range-color  {
    background-color: var(--color);
}

#slider .rs-path-color  {
    background-color: #382d5f;
    border-radius: 0;
}

#slider .rs-seperator  {
    display: none;
}

#slider .rs-handle  {
    background-color: var(--color);
}

#slider .rs-border  {
    border: 4px solid #382d5f;
}

#slider .rs-bg-color {
    background-color: #111;
}

#slider .rs-tooltip-text {
    font-size: 90px;
    text-align: center;
    transform: translate(-50%, -50%);
    margin: 0 !important;
    padding: 0;
    color: var(--color);
    text-shadow : 0 0 calc(var(--on) * 5px ) var(--color-glow),
                  0 0 calc(var(--on) * 10px) var(--color),
                  0 0 calc(var(--on) * 20px) var(--color-dark),
                  0 0 calc(var(--on) * 40px) var(--color-dark);
    transition: all 100ms ease-out;
}

body {
    display: flex;
    flex-flow: column;
    align-items: center;
}

h1 {
    font-weight: bold;
    text-align: center;
    color: white;
    font-size: 2rem;
}

#bpm {
    color: white;
    position: absolute;
    text-align: center;
    top: 60%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 99;
    font-size: 1rem;
}
</style>
<script defer>
    const slider = $("#slider").roundSlider({
        radius: 160,
        width: 20,
        handleSize: "+10",
        sliderType: "min-range",
        value: "60",
        min: 40,
        max: 218
    });
    const sleep = ms => new Promise(r => setTimeout(r, ms));

    var bpm = 60;
    var is_on = 0;
    var interval = setInterval(() => {
        is_on = !is_on;
        document.documentElement.style.setProperty("--on", Number(is_on));
    }, 60000 / bpm);
    var counter = 1;
    console.log(interval);
    slider.on("update", ({ value }) => {
        bpm = value;
        document.documentElement.style.setProperty("--bpm", bpm);
        clearInterval(counter);
        var interval = setInterval(() => {
            is_on = !is_on;
            document.documentElement.style.setProperty("--on", Number(is_on));
        }, 60000 / bpm);
        counter++;
        sendSliderValue(value);
    });

    function sendSliderValue(value) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/sld:" + value, true);
        xhr.send();
    }

</script>
</html>
"""
bpm = 60;
# Function to perform the light show
def light_show():
    while True:
        timer = map_value(bpm, 60, 160, 125, 20)
        #oled.fill(0)
        #oled.text("BPM:" + str(bpm), 1, 1)
        #oled.show()
        
        iLED4.turn_on()
        iLED4.drawColon(False)
        iLED4.clear()
        iLED4.printFloat(bpm, 0, 10)
        
        for i in range(0, 8):
            np[i] = (255, 0, 0)
            np.write()
            sleep_ms(timer)
            np[i] = (0, 0, 0)
            np.write()
        spk.freq(950)
        spk.duty(700)
        sleep_ms(10)
        spk.duty(0)
        for i in range(7, -1, -1):
            np[i] = (255, 0, 0)
            np.write()
            sleep_ms(timer)
            np[i] = (0, 0, 0)
            np.write()
        spk.duty(700)
        sleep_ms(10)
        spk.duty(0)

# Start the light show in a new thread
import _thread
_thread.start_new_thread(light_show, ())

# Setup socket for handling web requests
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Main loop for handling web requests
while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    if '/sld' in request:
        bpm = int(request[11:14])
        print('BPM:', bpm)
    conn.send(html)
    conn.close()



