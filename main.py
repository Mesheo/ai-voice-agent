import os
from record_audio import AudioHandler
from transcriber import transcribe_audio

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
                    print("Iniciando transcrição...")
                    transcript = transcribe_audio(filename)

                    print("\n📝 Transcrição:")
                    print(transcript)
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