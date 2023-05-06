from scipy.io import wavfile
import noisereduce as nr
from recorder import recording

recording(5)

rate, data = wavfile.read("example.wav")

reduced_noise = nr.reduce_noise(y=data, sr=rate)
wavfile.write("example_reduced_noise.wav", rate, reduced_noise)
