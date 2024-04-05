# Alex Ivensky
# ECE 1895
# Project 3
# Loopie 

import numpy as np
import pyaudio

CHUNK_SIZE = 1024


# Initialize PyAudio
p = pyaudio.PyAudio()

# Open input stream
stream_in = p.open(format=pyaudio.paInt16,
                   channels=1,
                   rate=44100,
                   input=True,
                   frames_per_buffer=CHUNK_SIZE)

# Open output stream
stream_out = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE)

try:
    while True:
        # Read data from input stream
        data = stream_in.read(CHUNK_SIZE)
        
        # Play the data through output stream
        stream_out.write(data)
        
except KeyboardInterrupt:
    pass

# Stop streams
stream_in.stop_stream()
stream_out.stop_stream()

# Close streams
stream_in.close()
stream_out.close()

# Terminate PyAudio
p.terminate()

