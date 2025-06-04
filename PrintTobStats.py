from math import floor
from statistics import mode
from statistics import stdev
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


# Times has to be SORTED
def printStats(times):
    averageDisplayTime = ticksToTime(np.average(times))
    print("Average Time: ", averageDisplayTime)

    modeDisplayTime = ticksToTime(mode(times))
    print("Mode: ", modeDisplayTime)
    if len(times) > 2:
        stdDevDisplayTime = ticksToTime(stdev(times))
        print("Std Dev:", stdDevDisplayTime)

    fastestTime = ticksToTime(times[0])
    print("Fastest Time: ", fastestTime)


# Times has to be SORTED for best results
def plotTimes(times, plotTitle, xLabelSize):
    displayTimes = ticksToDisplayTime(times)
    x = Counter(displayTimes).keys()
    y = Counter(displayTimes).values()

    plt.bar(x, y)
    plt.xlabel("Room Time")
    plt.ylabel("Trials")
    plt.title(plotTitle)
    if xLabelSize > 0:
        plt.tick_params(axis='x', which='major', labelsize=xLabelSize)
    plt.show()


def ticksToDisplayTime(times):
    timesInMinutes = []
    for x in range(len(times)):
        tick = times[x]
        timesInMinutes.append(ticksToTime(tick))
    return timesInMinutes


def ticksToTime(tick):
    totalSeconds = tick * 0.6
    minutes = floor(totalSeconds / 60)
    seconds = round(totalSeconds % 60, 1)
    if seconds < 10:
        return str(minutes) + ":0" + str(seconds)
    else:
        return str(minutes) + ":" + str(seconds)