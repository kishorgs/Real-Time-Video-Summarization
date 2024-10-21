import React, { useState } from "react";
import Button from "../components/Button";
import VideoPreview from "../components/VideoPreview";
import { startRecording, stopRecording } from "../services/api";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const [isRecording, setIsRecording] = useState(false);
  const navigate = useNavigate();

  const handleStartRecording = async () => {
    setIsRecording(true);
    await startRecording();
  };

  const handleStopRecording = async () => {
    setIsRecording(false);
    const summary = await stopRecording();
    navigate("/summary", { state: { summary } });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-6">Real-Time Video Summarization</h1>
      <div className="flex justify-center w-full max-w-md mb-6">
        <VideoPreview isRecording={isRecording} />
      </div>
      <div className="flex space-x-4">
        {!isRecording ? (
          <Button
            onClick={handleStartRecording}
            label="Start Recording"
            className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded shadow transition duration-200"
          />
        ) : (
          <Button
            onClick={handleStopRecording}
            label="Stop Recording"
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded shadow transition duration-200"
          />
        )}
      </div>
    </div>
  );
};

export default Home;
