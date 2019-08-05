# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:36:39 2019

Python Version: 3.x

Script to Generate Continuous-Phase FSK waveforms for Bell 103 and V.21 Modems

"""

import wave
import math
import struct
import random
    
def NextBitGenerator(option):
    if option == 'mark':
        while 1:
            yield 1
    if option == 'space':
        while 1:
            yield 0
    if option == 'square':
        bit = 0
        while 1:
            if bit == 0:
                bit = 1
            else:
                bit = 0
            yield bit
    if option == 'random':
        while 1:
            yield random.getrandbits(1)
    if option == 'ascii':
        while 1:
            text = b'This is a test message\r\n'
            index = 0
            bitindex = 0
            for i in range(0,300):  # sync first
                yield 1
            for index in range(0,len(text)):
                yield 0 # start bit
                for bitindex in range(7,-1,-1):
                    yield (text[index]>>(bitindex)) & 1
                yield 1 # stop bit

def CreateWavFile(mark, space, bitrate, filename, duration, option):
    print('Writing '+filename+'...')
    f1 = space # cycles/sec
    f2 = mark # cycles/sec
    fout = 44100.0 # samples/sec
    
    dphase = [f1/fout, f2/fout]
    
    wavfile = wave.open(filename,'wb')
    wavfile.setparams((1, 2, fout, 0, 'NONE', 'not compressed'))

    values = bytearray()
    phase = 0.0

    bitgen = NextBitGenerator(option)
    
    for j in range(0,int(duration*bitrate)): # bits
        bit = next(bitgen)
        for i in range(0,int(fout/bitrate)): # samples/bit
            value = int(30000.0*math.sin(phase*2*math.pi))
            phase = phase + dphase[bit]
            if phase > 1.0:
                phase = phase - 1.0
            packed_value = struct.pack('h', int(value))
            values.extend(packed_value)

    wavfile.writeframes(bytes(values))
    wavfile.close()
    print('Done!')

CreateWavFile(1270.0, 1070.0, 300.0, 'bell103_originate_mark.wav', 60.0, 'mark')
CreateWavFile(1270.0, 1070.0, 300.0, 'bell103_originate_space.wav', 60.0, 'space')
CreateWavFile(2225.0, 2025.0, 300.0, 'bell103_answer_mark.wav', 60.0, 'mark')
CreateWavFile(2225.0, 2025.0, 300.0, 'bell103_answer_space.wav', 60.0, 'space')

CreateWavFile(1270.0, 1070.0, 300.0, 'bell103_300bps_originate_random.wav', 60.0, 'random')
CreateWavFile(1270.0, 1070.0, 300.0, 'bell103_300bps_originate_square.wav', 60.0, 'square')
CreateWavFile(1270.0, 1070.0, 300.0, 'bell103_300bps_originate_ascii.wav', 60.0, 'ascii')
CreateWavFile(2225.0, 2025.0, 300.0, 'bell103_300bps_answer_random.wav', 60.0, 'random')
CreateWavFile(2225.0, 2025.0, 300.0, 'bell103_300bps_answer_square.wav', 60.0, 'square')
CreateWavFile(2225.0, 2025.0, 300.0, 'bell103_300bps_answer_ascii.wav', 60.0, 'ascii')

CreateWavFile(1270.0, 1070.0, 110.0, 'bell103_110bps_originate_random.wav', 60.0, 'random')
CreateWavFile(1270.0, 1070.0, 110.0, 'bell103_110bps_originate_square.wav', 60.0, 'square')
CreateWavFile(1270.0, 1070.0, 110.0, 'bell103_110bps_originate_ascii.wav', 60.0, 'ascii')
CreateWavFile(2225.0, 2025.0, 110.0, 'bell103_110bps_answer_random.wav', 60.0, 'random')
CreateWavFile(2225.0, 2025.0, 110.0, 'bell103_110bps_answer_square.wav', 60.0, 'square')
CreateWavFile(2225.0, 2025.0, 110.0, 'bell103_110bps_answer_ascii.wav', 60.0, 'ascii')

CreateWavFile( 980.0, 1180.0, 300.0, 'V.21_first_mark.wav', 60.0, 'mark')
CreateWavFile( 980.0, 1180.0, 300.0, 'V.21_first_space.wav', 60.0, 'space')
CreateWavFile(1650.0, 1850.0, 300.0, 'V.21_second_mark.wav', 60.0, 'mark')
CreateWavFile(1650.0, 1850.0, 300.0, 'V.21_second_space.wav', 60.0, 'space')

CreateWavFile( 980.0, 1180.0, 300.0, 'V.21_300bps_first_random.wav', 60.0, 'random')
CreateWavFile( 980.0, 1180.0, 300.0, 'V.21_300bps_first_square.wav', 60.0, 'square')
CreateWavFile( 980.0, 1180.0, 300.0, 'V.21_300bps_first_ascii.wav', 60.0, 'ascii')
CreateWavFile(1650.0, 1850.0, 300.0, 'V.21_300bps_second_random.wav', 60.0, 'random')
CreateWavFile(1650.0, 1850.0, 300.0, 'V.21_300bps_second_square.wav', 60.0, 'square')
CreateWavFile(1650.0, 1850.0, 300.0, 'V.21_300bps_second_ascii.wav', 60.0, 'ascii')

