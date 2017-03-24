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

import numpy as np
import os
import matplotlib.pyplot as plt

HRTF_head = []      # data of the ten experiments for the head
HRTF_mic = []       # data of the ten experiments for the AMVR design
numpoints = 2048    # don't really use this, but good to incorporate

#Number of bins and Sample frequency
gN = 2048
gf_sample = 44100

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
        for logchirp in data:
            _sum += logchirp[sample][1]
        average.append(_sum / 10)               # assuming num files = 10
    return average

# Simply returns a list of the frequency 
# divisons. Opens up the first HRTF_head example and pulls the division data from there.
# All frequency division information is assumed to be
# consistent across all experimental logchirp trials
def returnFrequencies():
    f = []
    for sample in range(2048):
        f.append(HRTF_head[0][sample][0])
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



#function to normalize
#Call this function with either HRTF_Head or HRTF_Mic lists
def NormalizeList(arr):
	norm_val = averageDecibels(arr)  #Generate 1D list with dBSPL values
	total = 0
	#calculate the mean value to offset by
	for i in range(2048):
		#norm_val[i] = 10**(norm_val[i]/20)
		total += norm_val[i]  
	# 	if (total == 0):
	# 		total = norm_val[i]
	# 	else:
	# 		total *= norm_val[i]
	mean = total/2048

	for i in range(2048):
		norm_val[i] = norm_val[i] - mean		# change from '-' to '/' --> linear to log scale
		#perform offset and convert to Gain from dBSPL
		norm_val[i] = 10**(norm_val[i]/20)
		
	#print (norm_val)						
	return norm_val
	
	
#Function to plot generic dbSPL vs Frequencies
def plotFreqSpectrum(freq, plt_arr, title_name, xlabel, ylabel):
	plt.semilogx(freq, plt_arr)
	#plt.ylim([-40, 40])
	plt.xlim([0, 22050])
	plt.grid(True,which="both",ls="-")
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.title(title_name)
	plt.show()
	
	
#Need to work on this method to get correct bin values
#Function to calculate bin values
def calcBins(arr, N, fs):
	binsize = fs/N
	
	numBins = N
	freq_list = returnFrequencies()
	
	binArray = []
	
	#for loops to iterate through bins and data values
	#Outer loop keeps track of bin number
	#Inner loop keeps track of data values 
	for k in range(numBins):
		cumulative = 0.0
		count = 0.0
		for i in range(2048):
			if(freq_list[i] > (binsize*k) and freq_list[i] < (binsize*(1+k))):
				#for each iteration in which a valid data point is found, the total is maintained
				#number of points is kept track of by count
				cumulative += arr[i]
				count += 1
		
		if(count == 0):
			binArray.append(binArray[k-1])
		
		else:
			avg_gainval = cumulative/count
			print(avg_gainval)
			binArray.append(avg_gainval)
		
	return binArray
			
	
def plotBinVals(yVal, N):
	#Generate x-axis for bin plot
	xfreq_list = []
	binSize = gf_sample/N
	xfreq_list.append(binSize/2)
	
	for i in range(N-1):
		xfreq_list.append(xfreq_list[i] + binSize)
		
	plt.plot(xfreq_list, yVal,'ro')
	plt.grid(True,which="both",ls="-")
	plt.xlim([0, 22050])
	plt.ylabel("Gain Values (per Bin)")
	plt.xlabel("Bin Frequency")
	plt.title("FFT Bin Gain")
	plt.show()

def generateTXT(name, arr):
	bins = open(name, "w+")   # create file if doesn't exist
	for bin in arr:
		bins.write(str(bin) + '\n')
	bins.close()

def main():
    #parse("Mic_12Oct_dBSPL_chirp3.txt", "h")
    #print(HRTF_head)
    
	openFiles()
	freq_list = returnFrequencies() #Generate frequency array
	
	xaxis_label = "Frequency (Hz)"
	
	averageMic = averageDecibels(HRTF_mic)
	averageHead = averageDecibels(HRTF_head)
	
	plotFreqSpectrum(freq_list, averageHead, "Binaural Head LogChirp Transfer Function", xaxis_label, "dBSPL")
	plotFreqSpectrum(freq_list, averageMic,"Binaural Head w AMVR Design LogChirp Transfer Function", xaxis_label, "dBSPL")

	
	#Generate normalized lists for Head, Mic and Differential
	Norm_head = NormalizeList(HRTF_head)
	Norm_mic = NormalizeList(HRTF_mic)
	plotFreqSpectrum(freq_list, Norm_head,"Normalized Head Plot", xaxis_label, "Gain (V/V)")
	plotFreqSpectrum(freq_list, Norm_mic, "Normalized Mic Plot", xaxis_label, "Gain (V/V)")
	
	#Calculate Head-Mic Difference
	#Gain_needed = Head/Mic
	Norm_HeadMic_diff = (np.array((Norm_head)) / np.array((Norm_mic))).tolist()			
	plotFreqSpectrum(freq_list, Norm_HeadMic_diff, "Head-Mic Gain Scaling/Restoration Plot", xaxis_label, "Gain (V/V)")
	
	bin_values = calcBins(Norm_HeadMic_diff, gN, gf_sample)
	generateTXT("bins.txt", bin_values)
	plotBinVals(bin_values, gN)
	

#Run main function
#Generate plots, note that all normalized plots have Gain values (not dBSPL)
main()

        
