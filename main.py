import os
from tqdm import tqdm
from googletrans import Translator
import whisper
import shutil

# site para baixar videos do YouTube
#https://ummy.net/pt33ZN/

def initialize_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[H\033[J')  # Código ANSI para limpar o terminal
    print("Aguarde... Em breve o programa irá iniciar!")
    print()

def translate_transcription(texto):
    destiny = "pt"
    translator = Translator()
    try:
        translation = translator.translate(texto, dest=destiny)
        return translation.text
    except Exception as e:
        # Handle the exception gracefully, e.g., print an error message
        print(f"Translation error: {e}")
        return f"Translation Error: {e}"

def process_video_file(video_file_path, output_srt_file_path):
    print("Aguarde... Carregando video para ser processado pela I.A.")
    model = whisper.load_model("small")
    audio = whisper.load_audio(video_file_path)
    result = model.transcribe(audio, fp16=False, language="en")

    with open(output_srt_file_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(tqdm(result["segments"], desc="Processing", unit="segment"), start=1):
            start_time = segment["start"]
            end_time = segment["end"]
            transcription = segment["text"]

            start_time_str = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{int(start_time % 60):02d},{int((start_time % 1) * 1000):03d}"
            end_time_str = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{int(end_time % 60):02d},{int((end_time % 1) * 1000):03d}"

            text_translated = translate_transcription(transcription)

            srt_file.write(f"{i}\n{start_time_str} --> {end_time_str}\n{text_translated}\n\n")
    


def process_all_mp4_files(directory_path):
    print("Procurando videos...")
    size_files = [file for file in os.listdir(directory_path) if not file.startswith('.')]

    if len(size_files) == 0:
        print("Nenhum video encontrado")

    for filename in os.listdir(directory_path):
        if filename.endswith(".mp4"):
            print()
            print("Video encontrado -> " + filename)
            video_file_path = os.path.join(directory_path, filename)
            output_srt_file_path = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}.srt")
            process_video_file(video_file_path, output_srt_file_path)
            print("Video legendado com sucesso -> " + filename)



def check_folder(pasta_origem, pasta_destino):

    for arquivo in os.listdir(pasta_origem):
        if arquivo != '.gitkeep':  # Ignora o arquivo .gitkeep
            shutil.move(os.path.join(pasta_origem, arquivo), pasta_destino)
            print(arquivo + " movido para pasta \"completed\"")

                    
    
    print()
    print("Programa encerrado")

# Specify the directory containing your MP4 files
current_directory = os.getcwd()
source_folder = current_directory + "/target"
destination_folder = current_directory + "/completed"

# Process all MP4 files in the specified directory
initialize_terminal()
process_all_mp4_files(source_folder)
check_folder(source_folder, destination_folder)