# Real-Time Video Summarization with FastAPI and React

This project enables real-time video recording, audio transcription, and automatic summarization using a combination of FastAPI for the backend and React for the frontend. The FastAPI backend handles video recording, transcription, and summarization, while the React frontend interacts with the backend through API endpoints for starting and stopping the recording.

## Features

- **Real-Time Video Recording**: Capture video and audio in real-time using the system's webcam and microphone.
- **Audio Transcription**: Converts recorded audio into text using Google Speech Recognition.
- **Text Summarization**: Generates a summary of the transcribed text using a generative AI model (Gemini 1.5).
- **React Frontend**: A React.js frontend allows users to start and stop video recording.
- **CORS Support**: Backend configured to support communication between FastAPI and the React frontend.

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- FastAPI
- React.js
- Pip for installing Python packages

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kishorgs/video-summarization.git
   cd video-summarization/backend
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install fastapi uvicorn pyaudio moviepy pydub SpeechRecognition google-generativeai opencv-python-headless
   ```

4. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

   This will start the server on `http://localhost:8000`.

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm start
   ```

   This will start the React frontend on `http://localhost:3000`.

## Usage

1. Start the backend FastAPI server on `http://localhost:8000`.
2. Run the React frontend on `http://localhost:3000`.
3. Use the frontend to start and stop video recordings.
4. When the recording is stopped, the system will generate a transcription and a summary of the recorded video.
5. The summarized text will be returned in the frontend upon stopping the recording.

## API Endpoints

- **Start Recording**:  
  `GET /start_recording`  
  Starts the video and audio recording process.

- **Stop Recording**:  
  `GET /stop_recording`  
  Stops the recording, merges audio and video, performs transcription, and returns a summary of the recorded content.

- **Video Feed**:  
  `GET /video_feed`  
  Streams the real-time video feed.

## Project Structure

```
.
├── backend                 # FastAPI backend code
│   ├── main.py             # Main FastAPI app
│   ├── recording.py        # Video/audio recording and summarization logic
│   └── temp_files          # Temporary files for audio/video storage
├── frontend                # React frontend code
│   ├── src
│   │   ├── api.js          # API request functions
│   │   ├── App.js          # Main React component
│   │   ├── components      # Reusable components
│   │   │   ├── Button.js   # Button component
│   │   │   └── VideoPreview.js  # Video preview component
│   │   ├── pages           # Page components for different views
│   │   │   ├── Home.js     # Home page for recording control
│   │   │   └── Summary.js  # Summary page for displaying video summary
│   └── package.json        # Frontend dependencies
├── README.md               # Project documentation
```

## Notes

- The transcription uses Google Speech Recognition, and the summarization leverages a Google Gemini model.
- Video is captured using OpenCV, and audio is recorded using PyAudio.
