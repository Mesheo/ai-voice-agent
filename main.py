from record_audio import AudioHandler
from transcriber import transcribe_audio
from ai_response import get_gpt_response

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
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                try:
                    seconds = float(input("Enter recording duration in seconds: "))
                    audio.record(seconds)
                    print("Iniciando transcrição...")
                    transcript = transcribe_audio(filename)

                    print("\n📝 Transcrição do seu áudio:")
                    print(transcript)

                    print("\n📝 Resposta do GPT: ")
                    get_gpt_response(transcript)
                except ValueError:
                    print("Please enter a valid number of seconds.")
            
            elif choice == '2':
                audio.play()
            
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