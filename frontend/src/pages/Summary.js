import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Button from "../components/Button";

const Summary = () => {
  const location = useLocation();
  const { summary } = location.state || {};
  const navigate = useNavigate();

  const goBack = () => {
    navigate("/");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-extrabold text-gray-800 mb-4">Summary</h2>
      <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
        {summary ? (
          <p className="mt-4 text-lg text-gray-700">{summary}</p>
        ) : (
          <p className="mt-4 text-lg text-gray-700">No summary available</p>
        )}
      </div>
      <Button
        onClick={goBack}
        label="Back"
        className="mt-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg shadow transition duration-200"
      />
    </div>
  );
};

export default Summary;
