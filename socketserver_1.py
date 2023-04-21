import asyncio
import websockets
import shutil
import time
from PIL import Image
import numpy as np
import mediapipe as mp
from keras.models import Sequential
from keras.layers import LSTM, Dense
# from keras.callbacks import TensorBoard
from mpdetection import mediapipe_detection, draw_styled_landmarks, extract_keypoints, getFrame

actions = np.array(['hello', 'thanks', 'iloveyou'])

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))
model.load_weights('action_nick.h5')

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities

def writeTofile(data, filename, i, seconds):
    # Convert binary data to proper format and write it on Hard Disk
        seconds=str(seconds)
        with open("test/"+filename+str(i)+".bmp", 'wb') as file:
            file.write(data)

def getFrame(i):
        with Image.open("test/"+"frame"+str(i)+".bmp") as image:
            frame = np.array(image)
            # print(frame.shape)
        return frame

async def handler(websocket, path):
    i = 0
    try:
        shutil.rmtree("./test")
        print(f'Successfully deleted folder')
    except: 
        pass
    try:
        shutil.os.mkdir("./test")
        print("created")
    except:
        pass

    sequence = []
    sentence = []
    predictions = []
    threshold = 0.5
    
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while (True):
            i=i+1
            data = await websocket.recv()
            
            seconds = time.time()
            # print("atharva chaman")
            # print(data)
            writeTofile(data, "frame",i,seconds)    
            frame=getFrame(i)
            # print("atharva chaman")
            if(i==10):
                 with Image.open("test/"+"frame"+str(i)+".bmp") as image:
                    pic = np.array(image)
                    pic2 = Image.fromarray(pic)
                    pic2.save("examples.bmp")
            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)

            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                if res[np.argmax(res)] > threshold: 
                    print(actions[np.argmax(res)])
                    predictions.append(np.argmax(res))

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

        
start_server = websockets.serve(handler, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


# sentence.append(data)       #convert data directly to numpy
            # frame = np.array(sentence[i])
           
                #  frame.save("examples.bmp")