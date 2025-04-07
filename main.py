import pyaudio
import wave
import sys
import os

class AudioHandler:
    def __init__(self, output_filename="recording.wav"):
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.sample_chunk_size = 1024 # 1024 samples per chunk
        self.samples_per_second = 44100  
        self.channels = 1  # Mono
        self.output_filename = output_filename
        self.pyaudio = pyaudio.PyAudio()

    def record(self, seconds):
        """Record audio for the specified number of seconds."""
        print(f"Recording for {seconds} seconds...")
        
        stream = self.pyaudio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.samples_per_second,
            frames_per_buffer=self.sample_chunk_size,
            input=True
        )

        # Each chunk is a group of samples collected over a short time.
        # Since we're recording in mono, one sample = one value.
        # So each chunk contains 1024 samples, and we collect multiple chunks per second.
        frame_chunks = []  
        
        total_chunks_per_duration = int(self.samples_per_second / self.sample_chunk_size * seconds)
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
        wf.setframerate(self.samples_per_second)
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


def main():
    print("Terminal-based Audio Recorder and Player")
    print("=======================================")
    
    filename = "recording.wav"
    audio = AudioHandler(filename)
    
    try:
        while True:
            print("\nOptions:")
            print("1. Record audio")
            print("2. Play recorded audio")
            print("3. Change output filename")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                try:
                    seconds = float(input("Enter recording duration in seconds: "))
                    audio.record(seconds)
                except ValueError:
                    print("Please enter a valid number of seconds.")
            
            elif choice == '2':
                audio.play()
            
            elif choice == '3':
                new_filename = input("Enter new filename (should end with .wav): ")
                if not new_filename.endswith('.wav'):
                    new_filename += '.wav'

                old_filename = audio.output_filename
                if os.path.exists(old_filename):
                    try:
                        os.rename(old_filename, new_filename)
                        audio.output_filename = new_filename
                        print(f"Renamed file from '{old_filename}' to '{new_filename}'")
                    except Exception as e:
                        print(f"Error renaming file: {e}")
                else:
                    print(f"File '{old_filename}' does not exist, cannot rename.")
            
            elif choice == '4':
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    
    finally:
        audio.cleanup()
        print("Program terminated.")


if __name__ == "__main__":
    main()