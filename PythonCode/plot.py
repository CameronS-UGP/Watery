import matplotlib.pyplot as plt
current_time = [0,0] # [Hours, Mins]
previous_time = [0,0] # [Hours, Mins]
difference_time = [0,0] # [Hours, Mins]
timeThreshold = [1,0] # [Hours, Mins] #should default to 1 hour
weight_of_container_empty = 14 # needed for scales to be calabrated
weight_of_container_full = 514 # needed for scales to be calabrated
toldtodrink = False
def convertTime(time):
    hours = int(time[0:2])
    mins = int(time[4:])
    total = (hours*60) + mins
    return total
def plot(path):
    # plot the change in fluid level over time to show them there own drinking habbits
    data1 = []
    data2 = []
    fluid = weight_of_container_full  # assume container was full or read in the first value and set that as "full"
    totalDrank = 0
    with open(path, "r") as f:
        # read a line
        for i, a in enumerate(f.readlines()):
            data = a.split(",")

            time = data[0][1:] + ":" + data[1][:(len(data[1]) - 1)]
            # print(time)
            time = convertTime(time)
            # print("Old Fluid :",fluid)
            totalDrank += (int(data[2][:(len(data[2]) - 1)]))  # remove +i when actual data has been gathered
            fluid = fluid - (int(data[2][:(len(data[2]) - 1)]))  # remove +i when actual data has been gathered
            # print("New Fluid :",fluid)
            # print(fluid)
            # print(time)
            # plot it as a line graph
            data1.append(time)
            data2.append(fluid)

    plt.plot(data1, data2)
    plt.title("Change In Fluid Over a Day")
    plt.xlabel("Time (minutes) Of a Day")
    plt.ylabel("Fluid level of container")
    plt.grid(True)
    print(str(totalDrank) + "%")
    plt.savefig("ChangeInFluid.png")
    plt.show()

plot("data.txt")