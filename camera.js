const videoElement = document.createElement('video');
const canvasElement = document.createElement('canvas');
const context = canvasElement.getContext('2d');

// Start the video stream
navigator.mediaDevices.getUserMedia({ video: true })
  .then((stream) => {
    videoElement.srcObject = stream;
    videoElement.play();

    // Continuously capture frames from the video
    function captureFrame() {
      context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
      
      // Send the frame to Python for processing (using Streamlit's message system)
      const imageData = canvasElement.toDataURL('image/jpeg');
      window.parent.postMessage({ image_data: imageData }, '*');
      
      // Call the captureFrame again to continuously send frames
      requestAnimationFrame(captureFrame);
    }

    captureFrame();
  })
  .catch((err) => {
    console.error('Error accessing webcam: ', err);
  });
