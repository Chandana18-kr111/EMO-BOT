import os
import time
import speech_recognition as sr
import RPi.GPIO as GPIO

# ================= LED SETUP =================
RED = 17
GREEN = 27
BLUE = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

def set_led(r, g, b):
    GPIO.output(RED, r)
    GPIO.output(GREEN, g)
    GPIO.output(BLUE, b)

# ================= SERVO (PCA9685) =================
from adafruit_pca9685 import PCA9685
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

def move_servo(channel, angle):
    pulse = int(100 + (angle / 180.0) * 400)
    pca.channels[channel].duty_cycle = pulse * 16

# ================= SPEAK =================
def speak(text):
    print("Bot:", text)
    os.system(f'espeak "{text}"')

# ================= LISTEN =================
r = sr.Recognizer()

def listen():
    with sr.Microphone(device_index=3) as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return ""

# ================= EMOTION ACTIONS =================
def happy_mode():
    speak("You sound happy! Let's celebrate!")
    set_led(0, 1, 0)   # Green

    for i in range(2):
        move_servo(0, 0)
        time.sleep(0.5)
        move_servo(0, 90)
        time.sleep(0.5)

def sad_mode():
    speak("I think you are sad. Let's cheer up! Raise your hands and jump!")
    set_led(1, 0, 0)   # Red

    for i in range(2):
        move_servo(0, 180)
        time.sleep(0.5)
        move_servo(0, 90)
        time.sleep(0.5)

# ================= MAIN LOOP =================
speak("Hello, I am EMOBOT. Your AI therapy assistant.")

while True:
    command = listen()

    if "happy" in command:
        happy_mode()

    elif "sad" in command:
        sad_mode()

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        break

    else:
        speak("I did not understand. Please say happy or sad.")

GPIO.cleanup()
