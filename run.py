import RPi.GPIO as GPIO
import time
import datetime

# Constants
RECYCLE_START = datetime.datetime(2024, 3, 14)  # Our recycle day is on a Thursday
GARBAGE_DAY = RECYCLE_START.weekday()

# Pin Configuration
RED = 16
YELLOW = 20
GREEN = 21
BUTTON = 12
LED_PINS = [RED, YELLOW, GREEN]

# LED Status
LED_STATUS = {
    "recycling": RED,
    "glass": YELLOW,
    "rubbish": GREEN
}

# Setup GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_PINS, GPIO.OUT)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_clicked, bouncetime=200)

# LED Control Functions
def switch_on(colours):
    GPIO.output(colours, GPIO.HIGH)

def switch_off(colours):
    GPIO.output(colours, GPIO.LOW)

def all_off():
    switch_off(LED_PINS)

def flash_leds(colour, flash_rate):
    switch_on([RED, colour])
    if flash_rate > 0:
        for _ in range(flash_rate):
            time.sleep(1.0 / flash_rate)
            switch_off([RED, colour])
            time.sleep(1.0 / flash_rate)
            switch_on([RED, colour])
    else:
        time.sleep(2)
    time.sleep(2)
    all_off()

# Flashing Logic for Bin Collection
def recycling_week(flash_rate):
    print("Recycling Week")
    flash_leds(YELLOW, flash_rate)

def green_waste_week(flash_rate):
    print("Green Waste Week")
    flash_leds(GREEN, flash_rate)

# Button Callback
def button_clicked(pin_num):
    GPIO.remove_event_detect(BUTTON)
    check_bin_day()
    setup_gpio()  # Re-setup button event detection

# Check Bin Day Logic
def check_bin_day():
    today = datetime.datetime.today()
    today_weekday = today.weekday()
    flash_rate = 0

    if today_weekday == GARBAGE_DAY:
        flash_rate = 10
        print("Your bins should have gone out this morning!")

    elif (today_weekday + 1) % 7 == GARBAGE_DAY:
        flash_rate = 5
        print("Put your bins out tonight!")

    weeks_since_start = (today - RECYCLE_START).days // 7

    if weeks_since_start % 2 == 1:
        recycling_week(flash_rate)
    else:
        green_waste_week(flash_rate)

    all_off()  # Ensure all LEDs are off after processing

# Main Logic
def main():
    setup_gpio()
    print("Press the button to check what bins go out this week!")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        all_off()  # Turn off LEDs on exit
        GPIO.cleanup()

if __name__ == "__main__":
    main()
