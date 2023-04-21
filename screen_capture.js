// Connect to the WebSocket server
const socket = new WebSocket("ws://localhost:5000");

const videoElem = document.getElementById("video");
  // const logElem = document.getElementById("log");
  const startElem = document.getElementById("start-capture");
  const stopElem = document.getElementById("stop-capture");
  const canvasElem = document.getElementById('output_canvas');
  const canvasCtx = canvasElem.getContext('2d');
  const gestureOutput = document.getElementById("caption");

socket.addEventListener("open", e=>{
  console.log("Connected to server");



async function startCapture() {
  try {
    // Request permission to capture the screen
    const stream = await navigator.mediaDevices.getDisplayMedia({
      video: true,
      audio: false
    });
    videoElem.srcObject = stream
    // Create a new ImageCapture object from the video track in the media stream
    const videoTrack = stream.getVideoTracks()[0];
    const imageCapture = new ImageCapture(videoTrack);

    // Set the frame rate to capture frames at a specific interval
    const frameRate = 30; // Frames per second
    const frameInterval = 1000 / frameRate; // Milliseconds per frame

    // Grab frames at the specified interval
    setInterval(async () => {
      // Capture a frame from the screen as an ImageBitmap
      const imageBitmap = await imageCapture.grabFrame();

      // Convert the ImageBitmap to a Blob
      const blob = await imageBitmapToBlob(imageBitmap);

      // Send the Blob to the backend using WebSockets
      socket.send(blob);
    }, frameInterval);
  } catch (error) {
    // Handle the error
  }
}

startElem.addEventListener(
  "click",
  (evt) => {
    startCapture();
  },
  false
);

stopElem.addEventListener(
  "click",
  (evt) => {
    stopCapture();
  },
  false
);


// Helper function to convert an ImageBitmap to a Blob
function imageBitmapToBlob(imageBitmap) {
  return new Promise(resolve => {
    const canvas = document.createElement('canvas');
    canvas.width = imageBitmap.width;
    canvas.height = imageBitmap.height;
    const context = canvas.getContext('2d');
    context.drawImage(imageBitmap, 0, 0);
    canvas.toBlob(blob => {
      resolve(blob);
    }, 'image/png');
  });
}

})
// // Connect to the WebSocket server
// const socket = new WebSocket("ws://localhost:5000");

// // Request permission to capture the screen
// navigator.mediaDevices.getDisplayMedia({
//   video: true,
//   audio: false
// }).then(stream => {
//   // Create a new ImageCapture object from the video track in the media stream
//   const videoTrack = stream.getVideoTracks()[0];
//   const imageCapture = new ImageCapture(videoTrack);

//   // Set the frame rate to capture frames at a specific interval
//   const frameRate = 30; // Frames per second
//   const frameInterval = 1000 / frameRate; // Milliseconds per frame

//   // Grab frames at the specified interval
//   setInterval(() => {
//     // Capture a frame from the screen as an ImageBitmap
//     imageCapture.grabFrame().then(imageBitmap => {
//       // Convert the ImageBitmap to a Blob
//       imageBitmapToBlob(imageBitmap).then(blob => {
//         // Send the Blob to the backend using WebSockets
//         socket.send(blob);
//       });
//     });
//   }, frameInterval);
// }).catch(error => {
//   // Handle the error
// });

// // Helper function to convert an ImageBitmap to a Blob
// function imageBitmapToBlob(imageBitmap) {
//   return new Promise(resolve => {
//     const canvas = document.createElement('canvas');
//     canvas.width = imageBitmap.width;
//     canvas.height = imageBitmap.height;
//     const context = canvas.getContext('2d');
//     context.drawImage(imageBitmap, 0, 0);
//     canvas.toBlob(blob => {
//       resolve(blob);
//     }, 'image/png');
//   });
// }