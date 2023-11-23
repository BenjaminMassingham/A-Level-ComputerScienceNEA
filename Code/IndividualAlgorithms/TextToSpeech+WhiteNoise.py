#Importing the text to speech module
import pyttsx3

#Importing the math module to do standard scientific operations like square root that cannot easily be done using operands
import math   

#Importing numpy to allow the easy addition of matricis and more complex mathmatical operations
import numpy as np 

#Importing librosa to allow me to analyse .wav files 
import librosa

#Importing scipy so that I can write an array into a .wav file as a waveform
from scipy.io.wavfile import write

#Importing the random module to select a random voice
import random

#Initialising the Python Text to Speech Module
engine = pyttsx3.init()

#An array of all of the voice ID's that speak english
voicesID = [0,7,10,11,17,28,32,33,37,40,41]

#Creating the voices property, allowing me to change it
voices = engine.getProperty('voices')

#Pulling a random voices ID from the voicesID list
voiceID = voicesID[random.randint(0,len(voicesID))]

#Setting the engines speech to a random english speaker
engine.setProperty('voice', voices[voiceID].id)

#Setting the string that the process will output
string = 'KLM1018, Hold position, contact heathrow ground 121.9'

#Creating the output, processed string
output_string = ''

#A for loop to check through each letter of the input string
for count in range(len(string)):

    #Checks if the character is a number
    if string[count].isdigit():

        #If it is a number, it adds a space before the number
        output_string = output_string + f' {string[count]}'

    #Checks if the character is a dot
    elif string[count] == '.':

        #Changes the dot to the word 'point' so the text to speech reads it correctly
        output_string = output_string + ' point'

    #If none of the above statements apply, the character is added as is
    else:
        output_string = output_string + string[count]

#Saving the text to a wav file
engine.save_to_file(output_string, 'ATC_Communications/PilotOutgoing.wav')

#Running the tasks that are waiting
engine.runAndWait()

#When this function is given the desired sound to noise ratio and the signal file, this routine returns the required white noise that should be added to the signal to get the desired sound to noise ratio
def get_white_noise(signal,SNR) :
    
    #Calculating the root mean square of the signal
    RMS_s = math.sqrt(np.mean(signal**2))

    #Calculating what the root mean square value needs to be for my additive white noise
    RMS_n = math.sqrt(RMS_s**2/(pow(10,SNR/10)))

    #In white noise, over enough samples, the mean is always 0, therefore, the standard deviation of the noise is equal to the root mean square value of the noise
    STD_n = RMS_n

    #Creates the noise waveform by random values of white noise who's standard deviation is equal to or less than the desired value
    noise = np.random.normal(0, STD_n, signal.shape[0])

    #Returns the noise waveform
    return noise

#This subroutine takes the complex numpy array and converts it to two seperate polar arrays to make it easier for the program to understand and reduce the time complexity
def to_polar(complex_ar):
    return np.abs(complex_ar),np.angle(complex_ar)

#Setting the file name for the input file
signal_file = 'ATC_Communications/PilotOutgoing.wav'

#Inporting the signal file as a waveform in an array
signal, sr = librosa.load(signal_file)
signal = np.interp(signal, (signal.min(), signal.max()), (-1, 1))

#Getting the white noise at the desired sound to noise ratio of value 20
noise = get_white_noise(signal,SNR=20)

#Analysing the noise waveform returned into 1 numpy array
X = np.fft.rfft(noise)

#Converting the numpy array to two seperate polar arrays, radius and angle
radius, angle = to_polar(X)

#Combining the two waveforms and adding them together using basic matrix addition
signal_noise = signal + noise

#Writing my waveform array to a .wav file
write("ATC_Communications/PilotOutgoingProcessed.mp3", sr, signal_noise)