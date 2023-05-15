#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
from time import sleep

# Note: In order the use the scales, calibration sequence must be run before it
# can output a weight in grams.
class Board:
    # Instructions:
    # Upon creating Board() instance, pass the GPIO Broadcom numbering of the following
    # Board(Data, Clock, LED, Buzzer)
    def __init__(self, dt_pin, sck_pin, led_pin, buzz_pin):
        # Setup up HX711 object for board object
        try:
            GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering (Broadcom)
            # Create an object hx which represents your real hx711 chip
            # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
            newHx = HX711(dout_pin=dt_pin, pd_sck_pin=sck_pin)  # Note: Blue(SCK) to GPIO 5 and green (DT) to GPIO 6
            self.hx = newHx

        except (KeyboardInterrupt, SystemExit):
            print('Exiting Code: 1')

        # finally:
        #     GPIO.cleanup()

        self.led_pin = led_pin
        self.buzz_pin = buzz_pin

    def calibrateScale(self):
        try:
            GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
            # measure tare and save the value as offset for current channel
            # and gain selected. That means channel A and gain 128
            err = self.hx.zero()
            # check if successful
            if err:
                raise ValueError('Tare is unsuccessful.')

            reading = self.hx.get_raw_data_mean()
            if reading:  # always check if you get correct value or only False
                # now the value is close to 0
                print('Data subtracted by offset but still not converted to units:',
                      reading)
            else:
                print('invalid data', reading)

            # In order to calculate the conversion ratio to some units, in my case I want grams,
            # you must have known weight.
            input('Put known weight on the scale and then press Enter')
            reading = self.hx.get_data_mean()
            if reading:
                print('Mean value from HX711 subtracted by offset:', reading)
                known_weight_grams = input(
                    'Write how many grams it was and press Enter: ')
                try:
                    value = float(known_weight_grams)
                    print(value, 'grams')
                except ValueError:
                    print('Expected integer or float and I have got:',
                          known_weight_grams)

                # set scale ratio for particular channel and gain which is
                # used to calculate the conversion to units. Required argument is only
                # scale ratio. Without arguments 'channel' and 'gain_A' it sets
                # the ratio for current channel and gain.
                ratio = reading / value  # calculate the ratio for channel A and gain 128
                self.hx.set_scale_ratio(ratio)  # set ratio for current channel
                print('Ratio is set.')
            else:
                raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

        except (KeyboardInterrupt, SystemExit):
            print('Exiting Code: 1')

        # finally:
        #     GPIO.cleanup()

    def getCurrentWeight(self):
        try:
            GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

            # Read data several times and return mean value
            # subtracted by offset and converted by scale ratio to
            # desired units. In my case in grams.
            curWeight = self.hx.get_weight_mean(20)

            print(curWeight, 'g')

            return curWeight

        except (KeyboardInterrupt, SystemExit):
            print('Exiting Code: 1')

        # finally:
        #     GPIO.cleanup()

    def buzzLED_switchOn(self):
        try:
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(self.led_pin, GPIO.OUT)  # set up channel for LED
            GPIO.setup(self.buzz_pin, GPIO.OUT)  # set up channel for buzzer

            GPIO.output(self.led_pin, GPIO.HIGH)  # switch on LED
            GPIO.output(self.buzz_pin, GPIO.HIGH)  # switch on buzzer

        except (KeyboardInterrupt, SystemExit):
            print('Exiting Code: 1')

        # finally:
        #     GPIO.cleanup()

    def buzzLED_switchOff(self):
        try:
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(self.led_pin, GPIO.OUT)  # set up channel for LED
            GPIO.setup(self.buzz_pin, GPIO.OUT)  # set up channel for buzzer

            GPIO.output(self.led_pin, GPIO.LOW)  # switch off LED
            GPIO.output(self.buzz_pin, GPIO.LOW)  # switch off buzzer

        except (KeyboardInterrupt, SystemExit):
            print('Exiting Code: 1')

        # finally:
        #     GPIO.cleanup()

    def buzzLED_alarm(self, on_interval, off_interval, iterations):
        try:
            for i in range(iterations):
                # Switch on for given interval
                self.buzzLED_switchOn()
                sleep(on_interval)

                # Switch off for given interval
                self.buzzLED_switchOff()
                sleep(off_interval)

        except (KeyboardInterrupt, SystemExit):
            print('Exiting Code: 1')
