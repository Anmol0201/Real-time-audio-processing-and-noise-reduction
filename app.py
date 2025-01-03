import pyaudio
import wave
import numpy as np
import noisereduce as nr

# Parameters
FORMAT = pyaudio.paInt16  # Format for audio input
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate
CHUNK = 1024  # Buffer size
OUTPUT_FILENAME = "processed_audio.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Open output WAV file
wav_file = wave.open(OUTPUT_FILENAME, 'wb')
wav_file.setnchannels(CHANNELS)
wav_file.setsampwidth(audio.get_sample_size(FORMAT))
wav_file.setframerate(RATE)

print("Recording and processing audio... Press Ctrl+C to stop.")

try:
    while True:
        # Read raw audio data
        raw_data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(raw_data, dtype=np.int16)

        # Simulate noise reduction
        noise_profile = audio_data[:CHUNK]  # Example noise profile
        reduced_noise = nr.reduce_noise(y=audio_data, sr=RATE, y_noise=noise_profile)

        # Save processed audio to file
        wav_file.writeframes(reduced_noise.tobytes())

except KeyboardInterrupt:
    print("Processing stopped.")

# Close streams and files
stream.stop_stream()
stream.close()
audio.terminate()
wav_file.close()
print(f"Processed audio saved to {OUTPUT_FILENAME}.")