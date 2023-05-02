import pyaudio
import wave

format = pyaudio.paInt16
channels = 1
rate = 22050
frames_per_buffer = 4410

p = pyaudio.PyAudio()

# starts recording
def recording(seconds):
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=frames_per_buffer)

    print("Start recording...")

    frames = []
    for i in range (0, int(rate / frames_per_buffer * seconds)):
        data = stream.read(frames_per_buffer)
        frames.append(data)

    print("Recording has stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("example.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()
