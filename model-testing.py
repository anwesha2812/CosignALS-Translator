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

def writeTofile(folder, data, filename, i, seconds): #ap
    # Convert binary data to proper format and write it on Hard Disk
        seconds=str(seconds) #Test 3 - added seconds to filename
        with open(folder+"/"+filename+str(i)+".bmp", 'wb') as file:
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
    
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while (True):
            i=i+1
            data = await websocket.recv()
            seconds = time.time()
            
            # print("atharva chaman")
            # print(data)
            writeTofile("test",data, "frame",i,seconds)    
            frame=getFrame(i)
            frame_number.append(i)
            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)
            # img_bytes=image.tobytes()
            image = Image.fromarray(image)  #array to bits
            # writeTofile("plottedframes",img_bytes, "frame",i,seconds) 
            # if (True):
            image.save("plottedframes/"+"frame"+str(i)+".bmp")

#prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            frame_number = frame_number[-30:]

            if len(sequence) == 30:
                print(frame_number[29])
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                if res[np.argmax(res)] > threshold: 
                    # print(actions[np.argmax(res)])
                    # print(sequence) #ap
                    predictions.append(np.argmax(res))
#viz logic
                if np.unique(predictions[-10:])[0]==np.argmax(res): 
                    if res[np.argmax(res)] > threshold: 
                        if len(sentence) > 0: 
                            if actions[np.argmax(res)] != sentence[-1]:
                                sentence.append(actions[np.argmax(res)])
                        else:
                            sentence.append(actions[np.argmax(res)])

                if len(sentence) > 5: 
                    sentence = sentence[-5:]
            disp_sentence=' '.join(sentence)
            print(disp_sentence)
            await websocket.send(disp_sentence)
            
start_server = websockets.serve(handler, "localhost", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


# sentence.append(data)       #convert data directly to numpy
            # frame = np.array(sentence[i])
           
                #  frame.save("examples.bmp")