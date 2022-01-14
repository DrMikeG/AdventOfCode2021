# https://www.gaussianwaves.com/2020/01/how-to-plot-audio-files-as-time-series-using-scipy-python/

from scipy.io.wavfile import read #import the required function from the module
import matplotlib.pyplot as plt
import numpy as np
import sys


#seaFloor = [ parseInstruction(number) for number in open(f'{sys.path[0]}/input.txt', 'r')]
samplerate, data = read(f'{sys.path[0]}/../Track_00_04.wav')

samplerate #echo samplerate

data #echo data -> note that the data is a single dimensional array
duration = len(data)/samplerate


# only process the first 60%...
percent = 60
original_len = len(data)
trimmed_len = (int((percent/100)*original_len))
trimmed_data = data[0:trimmed_len]

windowedValues = []

print(trimmed_data[0])

for i in range(0,len(trimmed_data)-1000,1000):
    sum = 0
    for j in range(i,i+1000):
        #print(trimmed_data[j])
        #print(trimmed_data[j][0])
        sum += trimmed_data[j][0]
    sum = sum / 1000

    windowedValues.append(abs(sum))
    
new_len = len(windowedValues)
new_duration = len(windowedValues)/samplerate
print("New len is {}".format(new_len))


time = np.arange(0,new_duration,1/samplerate) #time vector

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
students = [23,17,35,29,12]
#langs = ['C', 'C++', 'Java', 'Python', 'PHP']
langs =[]
for i in range(0,len(windowedValues)):
    langs.append(chr(i))

ax.bar(langs,windowedValues)
#ax.bar(langs,windowedValues)
plt.show()


#plt.plot(time,windowedValues)
#plt.xlabel('Time [s]')
#plt.ylabel('Amplitude')
#plt.title('Track_00_04.wav')
#plt.show()