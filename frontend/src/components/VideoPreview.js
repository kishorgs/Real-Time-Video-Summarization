import React from "react";

const VideoPreview = ({ isRecording }) => {
  return (
    <div className="video-preview relative w-full max-w-md mx-auto">
      {isRecording ? (
        <img
          src="http://localhost:8000/video_feed"
          alt="Video Feed"
          className="w-full h-auto rounded-lg shadow-lg"
        />
      ) : (
        <div className="flex flex-col items-center justify-center w-full h-64 bg-gray-200 rounded-lg border-dashed border-4 border-gray-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-16 w-16 text-gray-500 mb-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 4v16m8-8H4"
            />
          </svg>
          <span className="text-gray-600 text-xl font-semibold">
            Recording Not Started
          </span>
        </div>
      )}
    </div>
  );
};

export default VideoPreview;
