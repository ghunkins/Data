# ECE SENIOR DESIGN | HRTF MEASURED FUNCTIONS
# Determing the difference in transfer function
# between measured data of the pure binaural head
# data and the mic / research headphones data appended
# to the binaural head. Data average for both cases over
# 10 trials with the same set-up. Right ear used. 
# Important measures:
# Output Voltage Level of the Clio: 0.218V
# Bela On-Board amplification: 30dB
# Num points = 2048

import numpy
import os
import matplotlib.pyplot as plt

HRTF_head = []      # data of the ten experiments for the head
HRTF_mic = []       # data of the ten experiments for the AMVR design
numpoints = 2048    # don't really use this, but good to incorporate

def openFiles():   
    head = open("HEAD.txt", "w+")   # create file if doesn't exist
    mic = open("MIC.txt", "w+")     # create file if doesn't exist               
    for filename in os.listdir(os.getcwd()):    # get the current working directory
        print(filename)
        if filename.endswith(".txt") and filename.startswith("Head"):
            HRTF_head.append(parse(filename))      # append that files 2048 points
            continue
        elif filename.endswith(".txt") and filename.startswith("Mic"):
            HRTF_mic.append(parse(filename))
            continue
    head.close()
    mic.close()

# returns a list of 2048 points, each corresponding
# 1-1 to the frequency list. Gives the average decibels
# of the 3D matrix given by summing each point across the 
# ten trials, dividing by ten to get the average, and repeating
# for each of the 2048 points
def averageDecibels(data):
    average = []
    for sample in range(2048):
        _sum = 0
        for i, logchirp in enumerate(data):
            #print(logchirp)
            #print(logchirp[0])
            #print(logchirp[sample-1][1])
            #print(logchirp[i][sample-1])
            _sum += logchirp[sample][1]
        #print("Appending: ", _sum / 10)
        average.append(_sum / 10)               # assuming num files = 10
    return average

# Simply returns a list of the frequency 
# divisons. Opens up the first HRTF_head example
# and pulls the division data from there. All
# frequency division information is assumed to be
# consistent across all experimental logchip trials
def returnFrequencies():
    f = []
    for sample in range(2048):
        #print(HRTF_head[0][sample-1][0])
        f.append(HRTF_head[0][sample][0])
    print(f)
    return f

# returns a 2D list, inner lists are
# individual data points for a given
# file or experimential logchirp trial
def parse(filename):
    arr = []
    f = open(filename, "r+")
    for i, line in enumerate(f):
        if (i == 0): continue;      # skip the first line
        arr.append([float(s) for s in line.split()])
    return arr

# plots the average data from the binaural head data
# across the 10 different trials
def plotAverageHead():
    freq = returnFrequencies()
    averageHead = averageDecibels(HRTF_head)
    plt.semilogx(freq, averageHead)             # change semilogx to plot if you want linear not log
    plt.ylim([40, 100])
    plt.xlim([20, 20000])
    plt.grid(True,which="both",ls="-")
    plt.ylabel("dbSPL")
    plt.xlabel("Frequency")
    plt.title("Binaural Head w/o AMVR Design")
    plt.show()

# plots the average data from the mic data 
# across the 10 different trials
def plotMic():
    freq = returnFrequencies()
    averageMic = averageDecibels(HRTF_mic)
    plt.semilogx(freq, averageMic)              # change semilogx to plot if you want linear not log
    plt.ylim([40, 100])
    plt.xlim([20, 20000])
    plt.grid(True,which="both",ls="-")
    plt.ylabel("dbSPL")
    plt.xlabel("Frequency")
    plt.title("Binaural Head w AMVR Design")
    plt.show()

# non-normalized mic and head differential
# simply for curiousity sake, need to normalize for
# usable data
def plotMicHeadDifferential():
    freq = returnFrequencies()
    micHeadDifferential = (numpy.array(averageDecibels(HRTF_head)) - numpy.array(averageDecibels(HRTF_mic))).tolist()
    plt.semilogx(freq, micHeadDifferential)             # change semilogx to plot if you want linear not log
    #plt.ylim([40, 100])
    plt.xlim([20, 20000])
    plt.grid(True,which="both",ls="-")
    plt.ylabel("dbSPL")
    plt.xlabel("Frequency")
    plt.title("Head-Mic Differential")
    plt.show()


def main():
    #parse("Mic_12Oct_dBSPL_chirp3.txt", "h")
    #print(HRTF_head)
    openFiles()
    plotAverageHead()
    plotMic()
    plotMicHeadDifferential()


main()

        
