import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.io import wavfile

def fft(x):
    N = len(x) #find length of the input
    if N == 1: #base case for recursion
        return x
    else:
        evenX = fft(x[::2]) #perform recursion on the even values
        oddX = fft(x[1::2]) #perform recursion on the even values

        factor = np.exp(-2j*np.pi*np.arange(N)/ N) #mathematical formula to calculate the factor that is required

        X = np.concatenate([evenX+factor[:int(N/2)]*oddX, evenX+factor[int(N/2):]*oddX])
        return X

def runFFT(audioFile):
    samplerate, data = wavfile.read(audioFile)
    #zero centres the data
    data = data - np.average(data)

    # This calculates the amount of empty data points to be added to the data to make the data be of length 2^n
    amount = int(2**(np.ceil(np.log2(len(data))))-len(data))

    #Creates an empty array of length amount to pad the data
    padding_array = np.empty(shape=(amount, 2))

    #adds the padding array to the data
    data = np.append(data, padding_array)

    #runs the fft on the data
    X=fft(data)
    return X, samplerate

def gen_sig(sample_rate): #generates a random signal for testing
    sample_interval = 1/sample_rate
    time = np.arange(0, 1, sample_interval)

    x=0

    amplitude = 3
    freq = 94
    x += amplitude*np.sin(2*np.pi*freq*time)

    amplitude = 2
    freq = 100
    x += amplitude*np.sin(2*np.pi*freq*time)


    return x, time

if __name__=='__main__':
    samplerate = 128
    x, t = gen_sig(samplerate)

    X = fft(x)

    N = len(X)
    n = np.arange(N)
    T = N/samplerate
    freq = n/T 

    n_oneside = N//2

    f_oneside = freq[:n_oneside]

    X_oneside =X[:n_oneside]/n_oneside

    plt.figure(figsize = (12, 6))
    plt.subplot(121)
    plt.stem(f_oneside, abs(X_oneside), 'b', markerfmt=" ", basefmt="-b")

    plt.subplot(122)
    plt.plot(t, X, 'r')

    plt.show()