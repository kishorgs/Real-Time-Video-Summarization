import os
import wave
import pyaudio
import threading
import moviepy.editor as mp
from pydub import AudioSegment
import speech_recognition as sr
import google.generativeai as genai
import cv2
import asyncio

recognizer = sr.Recognizer()

genai.configure(api_key="your_gemini_api_key")  

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

stop_recording_event = threading.Event()

output_directory = "temp_files"
os.makedirs(output_directory, exist_ok=True)

def record_audio(audio_output_file="real_time_audio.wav"):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    print("Recording audio...")
    frames = []

    while not stop_recording_event.is_set():  
        data = stream.read(1024)
        frames.append(data)

    print("Audio recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_output_file_path = os.path.join(output_directory, audio_output_file)
    wf = wave.open(audio_output_file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

async def capture_video(output_file="real_time_video.mp4"):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_output_file_path = os.path.join(output_directory, output_file)
    out = cv2.VideoWriter(video_output_file_path, fourcc, 20.0, (640, 480))

    print("Recording video...")

    while not stop_recording_event.is_set():  
        ret, frame = cap.read()
        if ret:
            out.write(frame)

    cap.release()
    out.release()
    print("Video recording finished.")

def merge_audio_video(video_file, audio_file, output_file='final_output.mp4'):
    video_file_path = os.path.join(output_directory, video_file)
    audio_file_path = os.path.join(output_directory, audio_file)
    output_file_path = os.path.join(output_directory, output_file)
    
    video_clip = mp.VideoFileClip(video_file_path)
    audio_clip = mp.AudioFileClip(audio_file_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_file_path, codec='libx264')

def transcribe_audio(audio_file_path):
    audio_file_path = os.path.join(output_directory, audio_file_path)
    audio = AudioSegment.from_file(audio_file_path)
    audio_duration = len(audio)
    segment_length = 60 * 1000  
    output_dir = os.path.join(output_directory, 'audio_segments')
    os.makedirs(output_dir, exist_ok=True)

    segment_counter = 0
    final_transcription = ""

    for start in range(0, audio_duration, segment_length):
        end = min(start + segment_length, audio_duration)
        segment = audio[start:end]
        segment_file_path = os.path.join(output_dir, f'segment_{segment_counter}.wav')
        segment.export(segment_file_path, format='wav')

        try:
            with sr.AudioFile(segment_file_path) as source:
                audio_data = recognizer.record(source)
                transcription = recognizer.recognize_google(audio_data)
                final_transcription += transcription + " "
        except sr.UnknownValueError:
            print(f"Could not understand audio in segment {segment_counter}")
        except sr.RequestError as e:
            print(f"Request error: {e}")
        segment_counter += 1

    return final_transcription.strip()

def summarize_text(text):
    prompt_message = text + "\n\nSummarize this text into points without adding any additional information or changing context. Use bullet points."
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt_message)
    return response.text.strip()

def start_recording():
    global stop_recording_event
    stop_recording_event.clear()  

    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()

    asyncio.run(capture_video("real_time_video.mp4"))

    stop_recording_event.set()
    audio_thread.join()  

def stop_recording():
    global stop_recording_event
    stop_recording_event.set() 

def real_time_video_summarization():
    merge_audio_video("real_time_video.mp4", "real_time_audio.wav", "final_output.mp4")

    transcription = transcribe_audio('real_time_audio.wav')

    summary = summarize_text(transcription)

    return transcription, summary

if __name__ == "__main__":
    try:
        start_recording()
    except KeyboardInterrupt:
        stop_recording()
