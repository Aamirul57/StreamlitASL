// camera.js
import React, { useRef, useEffect } from "react";
import { Streamlit } from "streamlit-component-lib";

const CameraComponent = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        })
        .catch(err => {
          console.error("Error accessing webcam: ", err);
          Streamlit.setComponentValue({ error: "Failed to access webcam" });
        });
    } else {
      console.error("Camera not supported");
      Streamlit.setComponentValue({ error: "Camera not supported" });
    }
  }, []);

  const captureFrame = () => {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL("image/png");
    Streamlit.setComponentValue({ image: dataUrl });
  };

  return (
    <div>
      <video ref={videoRef} width="100%" height="100%" />
      <button onClick={captureFrame}>Capture Frame</button>
    </div>
  );
};

export default CameraComponent;
