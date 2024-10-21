from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from recording import real_time_video_summarization, start_recording, stop_recording
import threading
import cv2
import asyncio

app = FastAPI()

# Allow CORS for communication with React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recording_thread = None  
video_capture_thread = None  
video_capture_running = False  

@app.get("/start_recording")
async def start_record():
    global recording_thread, video_capture_thread, video_capture_running
    if recording_thread is None:
        recording_thread = threading.Thread(target=start_recording)
        recording_thread.start()
        video_capture_thread = threading.Thread(target=video_feed)
        video_capture_thread.start()
        video_capture_running = True
        return {"message": "Recording started..."}
    return {"message": "Recording is already in progress."}

@app.get("/stop_recording")
async def stop_record():
    global recording_thread, video_capture_thread, video_capture_running
    if recording_thread is not None:
        stop_recording()  
        recording_thread.join()  
        recording_thread = None  
        video_capture_running = False  
        video_capture_thread.join()  
        video_capture_thread = None  
        
        try:
            transcription, summary = real_time_video_summarization()
            return {"summary": summary}
        except Exception as e:
            return {"error": str(e)}
    
    return {"message": "No recording in progress."}

def video_feed():
    global video_capture_running
    cap = cv2.VideoCapture(0)  
    while video_capture_running:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()  
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
    cap.release()

@app.get("/video_feed")
def video_feed_endpoint():
    return StreamingResponse(video_feed(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/")
def read_root():
    return {"message": "Backend for video summarization is running!"}


handler = Mangum(app)