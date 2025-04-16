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
        print(f"Recording for {seconds} seconds...")
        
        stream = self.pyaudio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.sample_rate,
            frames_per_buffer=self.sample_chunk_size,
            input=True
        )

        frame_chunks = []  
        
        total_chunks_per_duration = int( (self.sample_rate * seconds) / self.sample_chunk_size )
        for i in range(total_chunks_per_duration):
            data = stream.read(self.sample_chunk_size)
            frame_chunks.append(data)

            if i % 10 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()

        stream.stop_stream()
        stream.close()
        print("\nFinished recording")

        # Save the recorded data as a WAV file
        with wave.open(self.output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.pyaudio.get_sample_size(self.sample_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frame_chunks))

        print(f"Recording saved as {self.output_filename}")
    
    def cleanup(self):
        self.pyaudio.terminate()

    def play(self):
        if not os.path.exists(self.output_filename):
            print(f"Error: {self.output_filename} not found.")
            return

        print(f"Playing back {self.output_filename}...")
        
        # Abrir o arquivo WAV
        wf = wave.open(self.output_filename, 'rb')
        
        # Criação do fluxo para reprodução
        stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(wf.getsampwidth()),  # Lendo o formato do arquivo
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        
        # Ler dados do arquivo e escrever no fluxo
        data = wf.readframes(self.sample_chunk_size)
        
        while len(data) > 0:
            stream.write(data)  # Reproduzir o áudio
            data = wf.readframes(self.sample_chunk_size)  # Ler mais dados
        
        # Fechar o fluxo e o arquivo
        stream.stop_stream()
        stream.close()
        wf.close()
        print("Playback finished")

    def list_audio_devices(self):
        info = self.pyaudio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        print("\n ------- Available input devices: --------")
        for i in range(num_devices):
            device_info = self.pyaudio.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                print(f"Device {i}: {device_info.get('name')}")
        print("-------- -------- --------")