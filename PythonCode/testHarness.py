from bottleScale import Board
import RPi.GPIO as GPIO  # import GPIO


def printWeight(times):
    for i in range(times):
        print(raspberry_pi.hx.get_weight_mean(20))  # print current weight on scale

try:
    # set up scale
    raspberry_pi = Board(dt_pin=6, sck_pin=5, led_pin=16, buzz_pin=12)  # Note: Determine pins for LED and buzzer
    #raspberry_pi.calibrateScale()  # Calibrate scale to read grams

    #printWeight(10)
    raspberry_pi.buzzLED_alarm(on_interval=2, off_interval=1, iterations=3)
    

except (KeyboardInterrupt, SystemExit):
    print('Exiting Code: 1')

finally:
    GPIO.cleanup()
    