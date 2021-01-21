import wave
import numpy


# Read file to get buffer
ifile = wave.open("440.wav")
samples = ifile.getnframes()
audio = ifile.readframes(samples)

# Convert buffer to float32 using NumPy
audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)

# Normalise float32 array so that values are between -1.0 and +1.0
max_int16 = 2**15
audio_normalised = audio_as_np_float32 / max_int16
