import math
from essentia_test import *
import numpy
import essentia
import essentia.standard as std
import essentia.streaming as es

loader = std.MonoLoader(filename = 'rsf_kobol_expander_2-vco/audio/vco1/square +/vco1_6.0_sqr+.wav.wav')
audio = loader()
params = { 'frameSize': 2048, 'hopSize': 128, 'startFromZero': False, 'sampleRate': 44100,'maxnSines': 100,'magnitudeThreshold': -74,'minSineDur': 0.02,'freqDevOffset': 10, 'freqDevSlope': 0.001, 'maxFrequency': 550.,'minFrequency': 65.}

def cutFrames(params, input):
    if not 'validFrameThresholdRatio' in params:
        params['validFrameThresholdRatio'] = 0
    frameGen = std.FrameGenerator(input, frameSize = params['frameSize'], hopSize = params['hopSize'], validFrameThresholdRatio = params['validFrame'], startFromZero = params['startFromZero'])
    return [frame for frame in frameGen]

def cleaningHarmonicTracks(freqsTotal, minFrames, pitchConf):
    confThreshold = 0.5
    nFrames = freqsTotal.shape[0]
    begTrack = 0
    freqsClean = freqsTotal.copy()

    if(nFrames > 0):
        f = 0
        nTracks = freqsTotal.shape[1]
        
        for t in range(nTracks):

            if (freqsClean[f][t] <= 0) and (freqsClean[f+1][t] > 0):
                begTrack = f + 1

            if ((freqsClean[f][t] > 0 and freqsClean[f+1][t] <= 0) and ((f - begTrack) < minFrames)):
                for i in range(begTrack, f + 1):
                    freqsClean[i][t] = 0

            if pitchConf[f] < confThreshold:
                freqsClean[f][t] = 0

            f += 1

    return freqsClean

def framesToAudio(frames):
    audio = frames.flatten()
    return audio

def analHprModelStreaming(params, signal):
    
    pool = essentia.Pool()
    fcut = es.FrameCutter(frameSize = params['frameSize'], hopSize = params['hopSize'], startFromZero = params['startFromZero'])
    w = es.Windowing(type = 'hann')
    spec = es.Spectrum(size = params['frameSize'])

    pitchDetect = es.PitchYinFFT(frameSize = params['frameSize'], sampleRate  = params['sampleRate'])
    smanal = es.HprModelAnal(sampleRate = params['sampleRate'], hopSize = params['hopSize'], maxnSines = params['maxnSines'], magnitudeThreshold = params['magnitudeThreshold'], freqDevOffset = params['freqDevOffset'], freqDevSlope = params['freqDevSlope'], minFrequency =  params['minFrequency'], maxFrequency =  params['maxFrequency'])

    signal = numpy.append(signal, zeros(params['frameSize'] // 2))
    insignal = VectorInput(signal)

    insignal.data >> fcut.signal
    fcut.frame >> w.frame
    w.frame >> spec.frame
    spec.spectrum >> pitchDetect.spectrum

    fcut.frame >> smanal.frame
    pitchDetect.pitch >> smanal.pitch
    pitchDetect.pitch >> (pool, 'pitch')
    pitchDetect.pitchConfidence >> (pool, 'pitchConfidence')
    smanal.magnitudes >> (pool, 'magnitudes')
    smanal.frequencies >> (pool, 'frequencies')
    smanal.phases >> (pool, 'phases')
    smanal.res >> (pool, 'res')

    essentia.run(insignal)

    mags = pool['magnitudes']
    freqs = pool['frequencies']
    phases = pool['phases']
    pitchConf = pool['pitchConfidence']

    minFrames = int(params['minSineDur'] * params['sampleRate'] / params['hopSize'])
    freqsClean = cleaningHarmonicTracks(freqs, minFrames, pitchConf)
    pool['frequencies'].data = freqsClean

    return mags, freqsClean, phases

m, f, p = analHprModelStreaming(params, audio)