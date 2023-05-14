from bottleScale import Board

def printWeight(times):
    for i in range(times):
        print(raspberry_pi.hx.get_weight_mean(20))  # print current weight on scale

# set up scale
raspberry_pi = Board(dt_pin=6, sck_pin=5, led_pin=9999, buzz_pin=9999)  # Note: Determine pins for LED and buzzer
raspberry_pi.calibrateScale()  # Calibrate scale to read grams

printWeight(35)
