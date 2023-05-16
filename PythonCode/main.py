import time
import math
import os
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from bottleScale import Board
from time import sleep
global timeThreshold

current_time = [0,0] # [Hours, Mins]
previous_time = [0,0] # [Hours, Mins]
difference_time = [0,0] # [Hours, Mins]
timeThreshold = [1,0] # [Hours, Mins] #should default to 1 hour
weight_of_container_empty = 14 # needed for scales to be calabrated
weight_of_container_full = 514 # needed for scales to be calabrated
toldtodrink = False


#check the time passed
#if the time passed is over a certain threshold tell the user to drink
#check fluid level
#if fluid level is too low tell the user to fill up there drink
#record the change in fluid level everytime they drink and the intervals they drink at
#graph the data so they can see their fluid intake over a day

def addtime(time, amount):
    #time is an array [hours, mins]
    #amount is an array [hours, mins]
    #returns an array [days, hours, mins]
    newHours = int(time[0]) + int(amount[0])
    newMins = int(time[1]) + int(amount[1])
    newDays = 0
    if(newMins > 59):
        newHours+=1
        newMins-=60
    if(newHours > 23):
        newHours-=24
        newDays+=1
    return [newDays, newHours, newMins]

def determineBottleWeights(raspberry_pi):
    print("""\n
Hi there! Welcome to Watery. Thank you for giving us a go. Before you can
use Watery, we need to know the weight of your bottle when it is empty and
when it filled up (or to the amount you usually fill it). To do so,
just follow the next 2 steps.

Step 1:
Please completely empty your water bottle (if it is not empty already) and
place it on the Watery measuring pad, then press Enter""")
    input()
    sleep(2)
    emptyWeight = raspberry_pi.hx.get_weight_mean(20)

    input("""
Step 2:
Next, please fill up your water bottle (or to where you normally fill it to)
and place it on the Watery measuring pad, then press Enter""")
    sleep(2)
    fullWeight = raspberry_pi.hx.get_weight_mean(20)
    print("\nThanks for completing the Watery set up.\n")

    return emptyWeight, fullWeight



#-------------------------------------------------------------------------
'''
What does our data mean?
What are we going to do with it?

Data.txt should clear after a week or have a mark for what day it is
Write toldToDrink to file so points on the graph can be marked

Plot fluid level against time not change in fluid level against time
the function that makes the graph should work out how accurate the warnings are 
- (did they drink when told to or did they leave it longer)
- (if they left it longer, how much longer)
- (was this wait consistent)
- (if it was, the time between warnings should be adjusted)
- (how much did they drink in a day)
- (did they drink enough according to national recommended average intake)

'''
def convertTime(time):
    hours = int(time[0:2])
    mins = int(time[4:])
    total = (hours*60) + mins
    return total

#[hours, mins], fluid
#[hours mins] fluid

def plot(path):
    #plot the change in fluid level over time to show them there own drinking habbits
    data1 = []
    data2 = []
    fluid = weight_of_container_full #assume container was full or read in the first value and set that as "full"
    totalDrank = 0
    with open(path,"r") as f:
        #read a line
        for i,a in enumerate(f.readlines()):
            data =  a.split(",")

            time = data[0][1:]+":"+data[1][:(len(data[1])-1)]
            #print(time)
            time = convertTime(time)
            #print("Old Fluid :",fluid)
            totalDrank += (int(data[2][:(len(data[2])-1)])) #remove +i when actual data has been gathered
            fluid = fluid - (int(data[2][:(len(data[2])-1)])) #remove +i when actual data has been gathered
            #print("New Fluid :",fluid)
            #print(fluid)
            #print(time)
            #plot it as a line graph
            data1.append(time)
            data2.append(fluid)
            
        
    plt.plot(data1,data2)  
    plt.title("Change In Fluid Over a Day")
    plt.xlabel("Time (minutes) Of a Day")
    plt.ylabel("Fluid level of container")
    plt.grid(True)
    print(str(totalDrank)+"%")
    plt.show()  

#plot("data.txt")    

def calabrate(path):
    #read in the data
    #look at "toldToDrink"
    #did the fluid change within 3 cycles of the warning
    #if yes leave the warning time as is
    #if not how often did this happen
    #if it happened more than once how long after the warning did they drink
    #adjust time to be closer to when they actually drank


    #did they drink the recommended national average
    #where they close to it?
    #if not make the time more frequent
    national_average = 1200 #ml (if fluid level is a percent then convert using weight of container)
    totalDrank = 0
    data2 = []
    with open(path,"r") as f:
        #read a line
        for i,a in enumerate(f.readlines()):
            data = a.split(",")
            #print(data)
            time = data[0][1:]+":"+data[1][:(len(data[1])-1)]
            #print("time",time)
            #print(time)
            time = convertTime(time)
            #print("Converted time",time)
            #print("Old Fluid :",fluid)
            fluidoverday = (int(data[2][:(len(data[2])-1)]))
            if fluidoverday > 0:
                totalDrank = fluidoverday
            #totalDrank += (int(data[2][:(len(data[2])-1)])) #remove +i when actual data has been gathered
            print("drank",totalDrank)
            data2.append([time,totalDrank])
    #figure out at what point they drank the national average
    #if they met this or got close to it by the end of the day (data set)
    #return
    prev_total = 0
    count = 0
    #print("Data",data2)
    for i,a in enumerate(data2):
        #print(data)
        #print("A",a[i])
        if(prev_total != a[1] and a[1] != 0): #if the total drank changed
            count+=1 # count the amount of times they drink
        prev_total = a[1]
        if(a[1] >= national_average):
            print("returning 0")
            return 0
    #print("Finished the for loop")
    if count == 0:
        count = 1
    average_drank = int(data2[-1][1]) / int(count)
    print("Average drank", average_drank)
    #work out the difference between nation average and total consumed
    diff_average = national_average - data2[-1][1]
    print("Diff average",diff_average)
    extra_drinks = 0
    if diff_average > 0 and average_drank > 0:
        #how many more time would they need to drink a day
        extra_drinks = diff_average / average_drank
    if extra_drinks == 0:
        return timeThreshold #if they have not drank anything yet, dont change the time
    #count is the amount of times they drank
    #they need to drink count+extra_drinks over the same time preiod
    #take the total time (in mins) and divide it by count+extra_drinks
    #print(data2[-1][0])
    newTimethreshold = math.ceil((convertTime("24:00") - int(data2[-1][0])) / extra_drinks)
    thing = [0,0]
    print("newtime",newTimethreshold)
    if(newTimethreshold > 60):
        thing[0] = math.floor(newTimethreshold/60)
        newTimethreshold = newTimethreshold%60
        thing[1] = newTimethreshold
    else:
        thing[0] = 0
        thing[1] = newTimethreshold
    #print(thing)
    return thing # represents the time threshold in the format [hours, mins]

try:
    # Note: Blue(SCK) to GPIO 5 and green (DT) to GPIO 6
    #       Blue(LED) to GPIO 16 and orange (BUzzer) to GPIO to 12

    print("------------------------- CALIBRATION OF LOAD CELL -------------------------")
    # set up scale
    raspberry_pi = Board(dt_pin=6, sck_pin=5, led_pin=16, buzz_pin=12)  # Note: Determine pins for LED and buzzer
    raspberry_pi.calibrateScale()  # Calibrate scale to read grams

    print("""
Please note, calibration is not part of the Watery functionality, it is
present because the load cell needs calibration at start of every runtime. 
The data for this could be saved, however, it is not currently implemented.
This would not be presented to the end user.
----------------------------------------------------------------------------""")

    weight_of_container_empty, weight_of_container_full = determineBottleWeights(raspberry_pi)
    print(weight_of_container_empty, weight_of_container_full)

    # getTime
    i = 1
    t = time.localtime()
    t = time.strftime("%H:%M:%S", t)

    previous_time = [int(t[0:2]), int(t[3:5])]
    # read in fluid level <------ after calibration this needs to happen
    current_fluid = raspberry_pi.hx.get_weight_mean(20) - weight_of_container_empty
    current_fluid = math.floor(current_fluid)
    previous_fluid = current_fluid
    while i!=0:
        toldtodrink = False
        t = time.localtime()
        t = time.strftime("%H:%M:%S", t)  # t[0:2] Hours t[3:5] Mins t[6:8] seconds
        print(t)
        hours = t[0:2]
        mins = t[3:5]
        current_time = [int(hours), int(mins)]
        #difference_time[0] += current_time[0] - previous_time[0]
        difference_time[1] += current_time[1] - previous_time[1]
        if (difference_time[1] > 59):
            difference_time[0] += 1
            difference_time[1] -= 60
        previous_time = current_time

        # check fluid level
        # compare current_fluid level and previous fluid level
        # record the differnce
        # if there is a change reset difference_time

        # ---------------- uncomment line below when weight can be read
        current_fluid = raspberry_pi.hx.get_weight_mean(20) - weight_of_container_empty  # <---- some function that returns the current weight
        # ----------------
        current_fluid = math.floor(current_fluid)
        print("Fluid:",current_fluid)
        #previous_fluid = math.floor(previous_fluid)
        #if current_fluid > (previous_fluid + 15):  # check if the container was filled
            #difference_fluid = current_fluid - previous_fluid
        if (previous_fluid - 5) < current_fluid < (previous_fluid + 7): #check if fluid hasn't change (with error)
            difference_fluid = 0
        else:
            difference_fluid = previous_fluid - current_fluid
        previous_fluid = current_fluid
        if difference_fluid != 0 and difference_fluid > 3:  # there was a change and the contain was not filled up
            difference_time = [0, 0]  # reset the timer

        if current_fluid < ((weight_of_container_full - weight_of_container_empty) * 0.2):  # if fluid level less than 20%
            raspberry_pi.buzzLED_alarm(on_interval=3, off_interval=1, iterations=3)

        # to run buzzer and LED alarm sequence
        # on_interval: how long it stays on for, and vice versa for off_interval (in seconds, floats can be used)
        # iterations is how many times it will do that

        # for example, buzzer and LED will sound/light for 2 seconds, the stay off for 2 seconds, 5 times
        # raspberry_pi.buzzLED_alarm(on_interval=2, off_interval=2, iterations=5)

        # set toldtodrink to true
        # if next cycle they drink mark it as true in the file
        # if they dont drink next cycle mark it as false
        
        print("Diff time:", difference_time)
        print("Diff fluid:", difference_fluid)
        print("Time Threshold:",timeThreshold, "\n")
        # check time
        if difference_time[0] >= timeThreshold[0]:
            #print("Testing First if")
            if difference_time[1] >= timeThreshold[1]:
                print("Flashing\n")
                raspberry_pi.buzzLED_alarm(on_interval=1, off_interval=1, iterations=3)
                toldtodrink = True
                difference_time = [0, 0]
                if (os.path.exists("data.txt")):
                    timeThreshold = calabrate("data.txt")
                #break  # remove after testing
        i += 1
        # write current_time,differnet_fluid to file
        write = str(current_time) + "," + str(difference_fluid)+"\n"
        with open("data.txt", 'a') as f:
            f.write(write)

        time.sleep(10)

except (KeyboardInterrupt, SystemExit):
    print('Exiting Code: 1')

finally:
    GPIO.cleanup()
#plot("data.txt")
#print(calabrate("data.txt"))
