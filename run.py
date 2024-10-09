import RPi.GPIO as GPIO
import time
import datetime

# Set a known date for recycling day
# (we assume recycling one week, green waste the next)
RECYCLE_START = datetime.datetime(2024, 3, 14)  # Our recycle day is on a Thursday
GARBAGE_DAY = RECYCLE_START.weekday()

# Set the pin numbers for each LED
RED = 16
YELLOW = 20
GREEN = 21

# Set the pin number for the button...
BUTTON = 12


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    set_GPIO_OUT()
    all_off()
    set_BUTTON_IN()


def set_GPIO_OUT():
    GPIO.setup([RED, YELLOW, GREEN], GPIO.OUT)


def switch_on(colours):
    set_GPIO_OUT()
    GPIO.output(colours, GPIO.HIGH)


def switch_off(colours):
    set_GPIO_OUT()
    GPIO.output(colours, GPIO.LOW)


def all_off():
    set_GPIO_OUT()
    switch_off([RED, YELLOW, GREEN])


def set_BUTTON_IN():
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_clicked,
                          bouncetime=200)


def flash_LEDs(colour, flash_rate):
    switch_on([RED, colour])
    if flash_rate > 0:
        for _ in xrange(flash_rate):
            time.sleep(1.0 / flash_rate)
            switch_off([RED, colour])
            time.sleep(1.0 / flash_rate)
            switch_on([RED, colour])
    else:
        time.sleep(2)
    time.sleep(2)
    all_off()


def recycling_week(flash_rate):
    print "Recycling Week"
    flash_LEDs(YELLOW, flash_rate)


def greenwaste_week(flash_rate):
    print "Green waste Week"
    flash_LEDs(GREEN, flash_rate)


def button_clicked(pin_num):
    # First let's stop checking for the button press...
    # We'll add the event detect back in after checking...
    GPIO.remove_event_detect(BUTTON)

    check_bin_day()
    # time.sleep(0.01) # Sleep a lil to avoid detecting phantom button presses...
    set_BUTTON_IN()


def check_bin_day():
    # Let's find out if tonight is bin night...
    today = datetime.datetime.today()

    print "Is it bin day today?"

    today_weekday = today.weekday()

    flash_rate = 0
    if (today_weekday == GARBAGE_DAY):
        flash_rate = 10
        print "Your bins should have gone out this morning!"

    if ((today_weekday + 1) % 7 == GARBAGE_DAY):
        flash_rate = 5
        print "Put your bins out tonight!"

    weeks_since_start = ((today - datetime.timedelta(days=1)) - RECYCLE_START).days / 7

    if ((weeks_since_start % 2) == 1):
        recycling_week(flash_rate)
    else:
        greenwaste_week(flash_rate)

    # Now make sure all LEDs are off
    all_off()


setup()

print "Press the button to check what bins go out this week!"

while True:
    time.sleep(0.1)
