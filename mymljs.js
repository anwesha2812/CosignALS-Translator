let url = "ws://localhost:5000"
const ws = new WebSocket(url);

  const videoElem = document.getElementById("video");
  // const logElem = document.getElementById("log");
  const startElem = document.getElementById("start-capture");
  const stopElem = document.getElementById("stop-capture");
  const canvasElem = document.getElementById('output_canvas');
  const canvasCtx = canvasElem.getContext('2d');
  const gestureOutput = document.getElementById("caption");
  ws.addEventListener("open", e=>{
    console.log("Connected to server");
  

  async function startCapture() {
    // logElem.innerHTML = "";
  
    try {
      var displayMediaOptions = {video:true }
       stream = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);
       videoElem.srcObject = stream
       videoElem.addEventListener("loadeddata", grabFrameLooper);
       
    } catch (err) {
      
    }
  }

  function stopCapture() {
    let tracks = videoElem.srcObject.getTracks();
    tracks.forEach((track) => track.stop());
    videoElem.srcObject = null;
  }
  
// Set event listeners for the start and stop buttons
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

async function grabFrameLooper(){
    const flag = true
    
    while (flag === true){
      await new Promise((resolve) => setTimeout(resolve, 50));
      // let tracks = videoElem.srcObject.getTracks();
      // track = tracks[0]
      // console.log(track.kind)
      // console.log(track.readyState)
      // if (waitForTrackLive(track)){
        // console.log("grabframe ke upar")
        grabFrame3()
        // console.log("grabframe ke neeche")
      // }
     
    }
}

async function waitForTrackLive(track) {
  while (track.readyState !== "live") {
    await new Promise(resolve => setTimeout(resolve, 50)); // wait for 100ms
  }
  // console.log("Track is now live!");
  return true
}

async function grabFrame3() {
  try {
    // console.log("weeeeeeeeeeeeeeeeeeeeeeeeeeeeee");
    // let tracks = videoElem.srcObject.getTracks();
    let tracks = stream.getVideoTracks()[0];
    track = tracks[0]
    console.log(track.kind)
    console.log(track.readyState)
    // waitForTrackLive(track)
    // console.log("wait for track ke neeche")
    if(true){
      let imageCapture = new ImageCapture(track);
      const imageBitmap = await imageCapture.grabFrame();
      console.log(imageBitmap)
      blob = imageBitmapToBlob(imageBitmap)
       var imageJSON = {
                                    imageBitmap: imageBitmap,        
                                }
          console.log(blob)
          ws.send(blob);

      // fetch("http://localhost/5000" + "/translate/", {

      //                               // Adding method type
      //                               method: "POST",

      //                               // Adding body or contents to send
      //                               body: JSON.stringify(imageJSON),

      //                               // Adding headers to the request
      //                               headers: {
      //                                   "Content-type": "application/json; charset=UTF-8"
      //                               },
      //                               mode: 'no-cors'
      //                           })
      //                               .catch(function (error) {
      //                               });
      // console.log("Grabbed frame:", imageBitmap);
      // console.log(window['i'])
      // window['i']=i+1
      // console.log("grabbedframeconsolelogkeneeche")
    }
    // canvas.width = imageBitmap.width;
    // canvas.height = imageBitmap.height;
    // canvas.getContext("2d").drawImage(imageBitmap, 0, 0);
    // canvas.classList.remove("hidden");
  } catch (error) {
    console.error("grabFrame() error: ", error);
  }
}

// function getImageCaptureObject(){
//   let tracks = videoElem.srcObject.getTracks();
//   track = tracks[0]
//   console.log(track.kind)
//   console.log(track.readyState)
//   let imageCapture = new ImageCapture(track);
//   grabFrame()
  // imageCapture.takePhoto()
  // while (track.readyState === "live"){
  // console.log("i work") grab image here
  // }



// function onResults(results) {
//   canvasCtx.save();
//   canvasCtx.clearRect(0, 0, canvasElem.width, canvasElem.height);
//   canvasCtx.drawImage(results.segmentationMask, 0, 0,
//                       canvasElem.width, canvasElem.height);

//   // Only overwrite existing pixels.
//   canvasCtx.globalCompositeOperation = 'source-in';
//   canvasCtx.fillStyle = '#00FF00';
//   canvasCtx.fillRect(0, 0, canvasElem.width, canvasElem.height);

//   // Only overwrite missing pixels.
//   canvasCtx.globalCompositeOperation = 'destination-atop';
//   canvasCtx.drawImage(
//       results.image, 0, 0, canvasElem.width, canvasElem.height);

//   canvasCtx.globalCompositeOperation = 'source-over';
//   drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS,
//                  {color: '#00FF00', lineWidth: 4});
//   drawLandmarks(canvasCtx, results.poseLandmarks,
//                 {color: '#FF0000', lineWidth: 2});
//   drawConnectors(canvasCtx, results.faceLandmarks, FACEMESH_TESSELATION,
//                  {color: '#C0C0C070', lineWidth: 1});
//   drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS,
//                  {color: '#CC0000', lineWidth: 5});
//   drawLandmarks(canvasCtx, results.leftHandLandmarks,
//                 {color: '#00FF00', lineWidth: 2});
//   drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS,
//                  {color: '#00CC00', lineWidth: 5});
//   drawLandmarks(canvasCtx, results.rightHandLandmarks,
//                 {color: '#FF0000', lineWidth: 2});
//   canvasCtx.restore();
// }

// function displayLandmarks(){

//   const holistic = new Holistic({locateFile: (file) => {
//     return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
//   }});
//   holistic.setOptions({
//     modelComplexity: 1,
//     smoothLandmarks: true,
//     enableSegmentation: true,
//     smoothSegmentation: true,
//     refineFaceLandmarks: true,
//     minDetectionConfidence: 0.5,
//     minTrackingConfidence: 0.5
//   });
//   holistic.onResults(onResults);

//   const detect = new Detect(videoElem, {
//     onFrame: async () => {
//       await holistic.send({image: videoElem});
//     },
//     width: 1280,
//     height: 720
//   });


// }




})
