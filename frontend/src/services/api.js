import axios from "axios";

const BASE_URL = "http://localhost:8000";

export const startRecording = async () => {
  try {
    await axios.get(`${BASE_URL}/start_recording`);
    console.log("Recording started...");
  } catch (error) {
    console.error("Error starting the recording:", error);
  }
};

export const stopRecording = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/stop_recording`);
    console.log("Recording stopped. Summary fetched.");
    return response.data.summary;
  } catch (error) {
    console.error("Error stopping the recording:", error);
  }
};
