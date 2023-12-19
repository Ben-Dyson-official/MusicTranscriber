import os
from pydub import AudioSegment
from pydub.utils import get_array_type
import scipy.fft
import scipy.signal
import array
import matplotlib.pyplot as plt
import numpy as np

def frequency_spectrum(sample, max_frequency=800):
    
    bit_depth = sample.sample_width * 8 #calculates bit depth of the audio
    array_type = get_array_type(bit_depth)
    raw_audio_data = array.array(array_type, sample._data)
    n = len(raw_audio_data)

    freq_array = np.arange(n) * (float(sample.frame_rate) / n)
    freq_array = freq_array[:(n // 2)] #normalise the frequency array
    raw_audio_data = raw_audio_data - np.average(raw_audio_data) #zero centering the data

    freq_magnitude = scipy.fft.fft(raw_audio_data) #runs the fourier transform on the audio
    
    freq_magnitude = freq_magnitude[:(n // 2)] #normalise the result of the fft

    if max_frequency:
        max_index = int(max_frequency * n / sample.frame_rate) + 1
        freq_array = freq_array[:max_index]
        freq_magnitude = freq_magnitude[:max_index]
    freq_magnitude = abs(freq_magnitude)
    freq_magnitude = freq_magnitude / np.sum(freq_magnitude)

    return freq_array, freq_magnitude

def get_notes(freq, chord):
    #defines the frequencies of the first octave which can calulate the frequency using frequency of the 1st octave times 2^which octave I want
    note_frequency =  {#A is 440Hz
        'C0':  16.35159783,
        'C#0': 17.32391444,
        'D0':  18.35404799,
        'D#0': 19.44543648,
        'E0':  20.60172231,
        'F0':  21.82676446,
        'F#0': 23.12465142,
        'G0':  24.49971475,
        'G#0': 25.9565436,
        'A0':  27.5,
        'A#0': 29.13523509,
        'B0': 30.86770633
    }
    TOLERANCE = 0.485 #sets tolerance for how wide the frequecny can be
    notesToReturn = ''
    # for i in range(8):
    i=4
    if freq>(note_frequency['C0']*(2**i)-TOLERANCE) and freq<(note_frequency['C0']*(2**i)+TOLERANCE)and('C'+str(i))not in chord:
        notesToReturn='C'+str(i)
    elif freq>(note_frequency['C#0']*(2**i)-TOLERANCE) and freq<(note_frequency['C#0']*(2**i)+TOLERANCE)and('C#'+str(i))not in chord:
        notesToReturn='C#0'+str(i)
    elif freq>(note_frequency['D0']*(2**i)-TOLERANCE) and freq<(note_frequency['D0']*(2**i)+TOLERANCE)and'D'+str(i)not in chord:
        notesToReturn='D'+str(i)
    elif freq>(note_frequency['D#0']*(2**i)-TOLERANCE) and freq<(note_frequency['D0']*(2**i)+TOLERANCE)and'D#'+str(i)not in chord:
        notesToReturn='D#'+str(i)
    elif freq>(note_frequency['E0']*(2**i)-TOLERANCE) and freq<(note_frequency['E0']*(2**i)+TOLERANCE)and'E'+str(i)not in chord:
        notesToReturn='E'+str(i)
    elif freq>(note_frequency['F0']*(2**i)-TOLERANCE) and freq<(note_frequency['F0']*(2**i)+TOLERANCE)and'F'+str(i)not in chord:
        notesToReturn='F'+str(i)
    elif freq>(note_frequency['F#0']*(2**i)-TOLERANCE) and freq<(note_frequency['F#0']*(2**i)+TOLERANCE)and'F#'+str(i)not in chord:
        notesToReturn='F#'+str(i)
    elif freq>(note_frequency['G0']*(2**i)-TOLERANCE) and freq<(note_frequency['G0']*(2**i)+TOLERANCE)and'G'+str(i)not in chord:
        notesToReturn='G'+str(i)
    elif freq>(note_frequency['G#0']*(2**i)-TOLERANCE) and freq<(note_frequency['G#0']*(2**i)+TOLERANCE)and'G#'+str(i)not in chord:
        notesToReturn='G#'+str(i)
    elif freq>(note_frequency['A0']*(2**i)-TOLERANCE) and freq<(note_frequency['A0']*(2**i)+TOLERANCE)and'A'+str(i)not in chord:
        notesToReturn='A'+str(i)
    elif freq>(note_frequency['A#0']*(2**i)-TOLERANCE) and freq<(note_frequency['A#0']*(2**i)+TOLERANCE)and'A#'+str(i)not in chord:
        notesToReturn='A#'+str(i)
    elif freq>(note_frequency['B0']*(2**i)-TOLERANCE) and freq<(note_frequency['B0']*(2**i)+TOLERANCE)and'B'+str(i)not in chord:
        notesToReturn='B'+str(i)
    elif freq>(note_frequency['C0']*(2**(i+1))-TOLERANCE) and freq<(note_frequency['C0']*(2**(i+1))+TOLERANCE)and('C'+str(i+1))not in chord:
        notesToReturn='C'+str(i+1)
    return notesToReturn

def predict_note_starts(audio, segment_ms, actual_notes=[]):
    #This function will use a heuristic method to predict when a note has started
    volume = [segment.dBFS for segment in audio[::segment_ms]] #gets an array of all the volumes of each audio section
    predicted_notes = [] #declares the list to be added to

    VOLUME_THRESHOLD = -35 #set minimum requirement to be considered a note
    EDGE_THRESHOLD  = 3.5 #sets the difference the volume should be to determin a note
    MIN_MS_BETWEEN = 100 #each note must have a difference between them

    for i in range(1, len(volume)):
        if volume[i]>VOLUME_THRESHOLD and volume[i]-volume[i-1]>EDGE_THRESHOLD:
            ms=i*segment_ms
            if len(predicted_notes)==0 or ms-predicted_notes[-1]>=MIN_MS_BETWEEN:
                predicted_notes.append(ms)
    return predicted_notes

def predict_notes(audio, predicted_starts, segment_ms): 
    #This function will predict the notes in the segmetns between each predicted start
    predicted_notes = []

    for i, start in enumerate(predicted_starts):
        sample_from = start + segment_ms 
        sample_to = start + 11*segment_ms
        if i < len(predicted_starts)-1: 
            sample_to = min(predicted_starts[i+1], sample_to)
        
        segment = audio[sample_from: sample_to] #makes the segment
        freq_array, freq_magnitude = frequency_spectrum(segment)

        peak_indicies, props = scipy.signal.find_peaks(freq_magnitude, height=0.0025) #finds the peaks of the frequencies
        average_height = np.average([props["peak_heights"][j]for j in range(len(props['peak_heights']))]) #finds the average hieght of the frequencies

        peak_indicies, props = scipy.signal.find_peaks(freq_magnitude, height=average_height) #find the peaks of the frequencies using the average height

        chord = []
        for i, peak in enumerate(peak_indicies):
            freq = freq_array[peak]
            magnitude = props["peak_heights"][i]
            note = get_notes(freq, chord)
            if note: chord.append(note)
            #print(f"{freq}Hz with magnitude {magnitude}")
        predicted_notes.append(chord)
    return predicted_notes

def mainMusicAnalysis(audioFile):

    audio = AudioSegment.from_file(audioFile) #make an object of the audio

    audio = audio.high_pass_filter(80) #remove background noise

    SEGMENT_MS = 50 #set the size of the segments

    predicted_starts = predict_note_starts(audio, SEGMENT_MS) #Get predicted starts

    predicted_notes = predict_notes(audio, predicted_starts, SEGMENT_MS) #get predicted notes

    return predicted_notes, predicted_starts

if __name__=='__main__':
    predicted_notes, predicted_starts = mainMusicAnalysis('/Users/bendyson/Coding/NEA/2 crotchets and a minim.wav') #2 crotchets and a minim

    print('Test 2.b.i: ')
    print(predicted_starts)

    predicted_notes, predicted_starts = mainMusicAnalysis('/Users/bendyson/Coding/NEA/4 quavers and a semibreve.wav') #4 quavers and a semibreve

    print('Test 2.b.ii: ')
    print(predicted_starts)






























    # freq_array, freq_magnitude = frequency_spectrum(audio)
    # plt.axhline(y=0.0025, color='r', linewidth=0.5, linestyle='-')
    # volume = [segment.dBFS for segment in audio[::SEGMENT_MS]]
    # x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
    # plt.plot(freq_array, freq_magnitude, 'b')
    # plt.plot(x_axis, volume, 'b')
    # plt.title('Chord C')
    # plt.xlabel('freq_array')
    # plt.ylabel('freq_magnitude')

    # plt.show()