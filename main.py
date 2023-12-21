import os
import whisper
from googletrans import Translator

# site para baixar videos do YouTube https://greenconvert.net/pt6/youtube-to-mp4

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
    model = whisper.load_model("small")
    audio = whisper.load_audio(video_file_path)
    result = model.transcribe(audio, fp16=False, language="en")

    with open(output_srt_file_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(result["segments"], start=1):
            start_time = segment["start"]
            end_time = segment["end"]
            transcription = segment["text"]

            start_time_str = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{int(start_time % 60):02d},{int((start_time % 1) * 1000):03d}"
            end_time_str = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{int(end_time % 60):02d},{int((end_time % 1) * 1000):03d}"

            text_translated = translate_transcription(transcription)

            srt_file.write(f"{i}\n{start_time_str} --> {end_time_str}\n{text_translated}\n\n")

    print(f"Arquivo SRT criado: {output_srt_file_path}")


def process_all_mp4_files(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".mp4"):
            video_file_path = os.path.join(directory_path, filename)
            output_srt_file_path = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}.srt")
            process_video_file(video_file_path, output_srt_file_path)


# Specify the directory containing your MP4 files
mp4_directory = "D:/Jetpack Compose/arroz/"

# Process all MP4 files in the specified directory
process_all_mp4_files(mp4_directory)
