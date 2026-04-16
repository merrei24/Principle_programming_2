import wave
import struct
import math

def create_sound(filename, freq):
    framerate = 44100
    duration = 4  # секунды
    amplitude = 32767

    wavef = wave.open(filename, 'w')
    wavef.setnchannels(1)
    wavef.setsampwidth(2)
    wavef.setframerate(framerate)

    for i in range(int(duration * framerate)):
        value = int(amplitude * math.sin(2 * math.pi * freq * i / framerate))
        data = struct.pack('<h', value)
        wavef.writeframesraw(data)

    wavef.close()

create_sound("track1.wav", 440)
create_sound("track2.wav", 660)