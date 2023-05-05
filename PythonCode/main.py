import time
import matplotlib.pyplot as plt
current_time = [0,0] # [Hours, Mins]
previous_time = [0,0] # [Hours, Mins]
difference_time = [0,0] # [Hours, Mins]
timeThreshold = [0,10] # [Hours, Mins]
current_fluid = 100 #%
previous_fluid = 100 #%
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

#getTime
i=0
t = time.localtime()
t = time.strftime("%H:%M:%S", t)

previous_time = [int(t[0:2]),int(t[3:5])]
while i!=0:
    t = time.localtime()
    t = time.strftime("%H:%M:%S", t) #t[0:2] Hours t[3:5] Mins t[6:8] seconds
    print(t)
    hours = t[0:2]
    mins = t[3:5]
    current_time = [int(hours),int(mins)]
    difference_time[0] += current_time[0] - previous_time[0]
    difference_time[1] += current_time[1] - previous_time[1]
    if(difference_time[1] >59):
        difference_time[0]+=1
        difference_time[1]-=60
    previous_time = current_time
    
    #check fluid level
    # compare current_fluid level and previous fluid level
    # record the differnce
    # if there is a change reset difference_time
    
    #read in fluid level
    if current_fluid > previous_fluid: #check if the container was filled
        difference_fluid = current_fluid
    else:
        difference_fluid = previous_fluid - current_fluid 
    previous_fluid = current_fluid
    if difference_fluid != 0 and difference_fluid > 0: #there was a change and the contain was not filled up
        difference_time = [0,0] #reset the timer


    '''
    if  fluid_level < 10%:
        alert the user to refill
    elif fluid_levle <2%:
        alert the user to refill continuosly
    '''
    #set toldtodrink to true
    #if next cycle they drink mark it as true in the file
    #if they dont drink next cycle mark it as false

    #check time
    if difference_time[0] > timeThreshold[0]:
        #alert user 
        toldtodrink = True
        difference_time = [0,0]
        break #remove after testing
    elif difference_time[0] == timeThreshold[0]:
        if difference_time[1] >= timeThreshold[1]:
            #alert user
            toldtodrink = True
            difference_time = [0,0]
            break #remove after testing
    i+=1
    # write current_time,differnet_fluid to file
    write = str(current_time)+","+str(difference_fluid)+"\n"
    with open("data.txt",'a') as f:
        f.write(write)
    
    time.sleep(10)


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
    with open(path,"r") as f:
        #read a line
        for i,a in enumerate(f.readlines()):
            data =  a.split(",")

            time = data[0][1:]+":"+data[1][:(len(data[1])-1)]
            #print(time)
            time = convertTime(time)
            fluid = int(data[2][:(len(data[2])-1)])+i
            #print(fluid)
            #print(time)
            #plot it as a line graph
            data1.append(time)
            data2.append(fluid)
            
        
    plt.plot(data1,data2)  
    plt.title("Fluid intake over a day")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Fluid level (%)")
    plt.grid(True)
    plt.show()    

plot("data.txt")

