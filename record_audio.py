import pyaudio
import wave
import sys
import os

class AudioHandler:
    def __init__(self, output_filename="recording.wav"):
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.sample_chunk_size = 1024 # 1024 samples per chunk
        self.sample_rate = 44100  
        self.channels = 1  # Mono
        self.output_filename = output_filename
        self.pyaudio = pyaudio.PyAudio()

    def record(self, seconds):
        """Record audio for the specified number of seconds."""
        print(f"Recording for {seconds} seconds...")
        
        stream = self.pyaudio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.sample_rate,
            frames_per_buffer=self.sample_chunk_size,
            input=True
        )

        # Each chunk is a group of samples collected over a short time.
        # Since we're recording in mono, one sample = one value.
        # So each chunk contains 1024 samples, and we collect multiple chunks per second.
        frame_chunks = []  
        
        total_chunks_per_duration = int( (self.sample_rate * seconds) / self.sample_chunk_size )
        for i in range(total_chunks_per_duration):
            print(i)
            data = stream.read(self.sample_chunk_size)
            frame_chunks.append(data)

            if i % 10 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()

        """
        We are basically saying to pyaudio: record to me 44100 samples in a second, every sample being 16bits in size,
        and return this data in chunks of 1024 samples        
        """
        stream.stop_stream()
        stream.close()
        print("\nFinished recording")

        # Save the recorded data as a WAV file
        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.pyaudio.get_sample_size(self.sample_format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frame_chunks))
        wf.close()
        
        print(f"Recording saved as {self.output_filename}")

    def play(self):
        """Play back the recorded audio file."""
        if not os.path.exists(self.output_filename):
            print(f"Error: {self.output_filename} not found.")
            return

        print(f"Playing back {self.output_filename}...")
        
        # Open the sound file
        wf = wave.open(self.output_filename, 'rb')
        
        # Create a stream for playback
        stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        
        # Read data in chunks
        data = wf.readframes(self.sample_chunk_size)
        
        # Play the sound by writing the audio data to the stream
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(self.sample_chunk_size)
            
        # Close and terminate
        stream.stop_stream()
        stream.close()
        print("Playback finished")

    def cleanup(self):
        self.pyaudio.terminate()

