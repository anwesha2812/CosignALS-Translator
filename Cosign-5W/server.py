import asyncio
import websockets
import mediapipe as mp
import shutil
from file_writing import writeTofile
import time
from mp_detection import mediapipe_detection, draw_styled_landmarks, extract_keypoints, getFrame
import numpy as np
from keras.models import Sequential
from PIL import Image
from keras.layers import LSTM, Dense
from prediction import predict

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities

actions = np.array(['hello', 'thanks', 'iloveyou', 'yes', 'no'])

model = Sequential()
model.add(LSTM(160, return_sequences=True, activation='relu', input_shape=(30,126)))
model.add(LSTM(224, return_sequences=True, activation='relu'))
model.add(LSTM(160, return_sequences=False, activation='relu'))
model.add(Dense(160, activation='relu'))
model.add(Dense(96, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.load_weights('action5words.h5')

async def handler(websocket, path):
    i=0
    try:
        shutil.rmtree("./test")
        shutil.rmtree("./plottedframes")#ap
        print(f'Successfully deleted folder')
    except: 
        pass
    try:
        shutil.os.mkdir("./test")
        shutil.os.mkdir("./plottedframes")#ap
        print("created")
    except:
        pass 

    sequence = []
    frame_number=[]
    sentence = []
    predictions = []
    threshold = 0.5

    while(True):
        i=i+1
        data = await websocket.recv()
        seconds= time.time()
        writeTofile("test", data, "frame", i, seconds)
        
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            frame=getFrame(i)
            frame_number.append(i)
            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)
            image = Image.fromarray(image)
            image.save("plottedframes/"+"frame"+str(i)+".bmp")

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            frame_number = frame_number[-30:]
#prediction logic
            if len(sequence) == 30:
                print(frame_number[29])
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions[np.argmax(res)])
                if res[np.argmax(res)] > threshold: 
                    predictions.append(np.argmax(res))

#viz logic
                if res[np.argmax(res)] > threshold: 
                    if len(sentence) > 0: 
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])

                if len(sentence) > 10: 
                    sentence = sentence[-10:]
            disp_sentence=' '.join(sentence)
            print(disp_sentence)
            await websocket.send(disp_sentence)
            
start_server = websockets.serve(handler, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
