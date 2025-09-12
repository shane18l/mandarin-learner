import React, { useState, useRef } from "react";
import { MediaRecorder, register } from 'extendable-media-recorder';
import { connect } from 'extendable-media-recorder-wav-encoder';

export default function App() {

  const [recording, setRecording] = useState(false);
  const [pred, setPred] = useState(null);

  const mediaRecorderRef = useRef(null);
  const chunks = useRef([]);

  const startRecording = async () => {
    await register(await connect());



    const stream = await navigator.mediaDevices.getUserMedia({ audio : true });
    mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: 'audio/wav' });

    // When audio becomes available, push to chunks
    mediaRecorderRef.current.ondataavailable = (e) => chunks.current.push(e.data);
    mediaRecorderRef.current.onstop = async () => {
      const blob = new Blob(chunks.current, { type: "audio/wav" });
      chunks.current = [];

      console.log("Blob type:", blob.type);     // should be 'audio/wav'
      console.log("Blob size:", blob.size);
          // Create a URL to play the audio
      const audioURL = URL.createObjectURL(blob);
      const audio = new Audio(audioURL);
      audio.controls = true; // optional if adding to DOM
      audio.play(); // automatically plays it

      // If you want to append to page
      const audioElement = document.createElement("audio");
      audioElement.src = audioURL;
      audioElement.controls = true;
      document.body.appendChild(audioElement);

      const formData = new FormData();
      formData.append("file", blob, "recording.wav");
      try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log(data);
      setPred(data);
    } catch (err) {
      console.error("Fetch error:", err);
    }

    }
    mediaRecorderRef.current.start();
    setRecording(true)
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <div className="App" style={{ textAlign: "center", padding: "2rem" }}>
      <h1>Mandarin Tone Tutor</h1>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {pred && (
        <div style={{ marginTop: "1rem" }}>
          <p>Predicted Tone: {pred.tone}</p>
          <p>Confidence: {(pred.probabilities ? Math.max(...pred.probabilities[0]) : 0).toFixed(2)}</p>
        </div>
      )}
    </div>
  );
}