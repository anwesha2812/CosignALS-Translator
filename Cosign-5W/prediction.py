# import mediapipe as mp

# mp_holistic = mp.solutions.holistic # Holistic model
# mp_drawing = mp.solutions.drawing_utils # Drawing utilities

# def predict(data):
#     i=0
#     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
#         while (True):
#             i=i+1
import mediapipe as mp
from PIL import Image
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from mp_detection import mediapipe_detection, draw_styled_landmarks, extract_keypoints, getFrame

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



def predict(j):
    sequence = []
    frame_number=[]
    sentence = []
    predictions = []
    threshold = 0.5

    # j=0
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            frame=getFrame(j)
            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)
            image = Image.fromarray(image)
            image.save("plottedframes/"+"frame"+str(j)+".bmp")

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
            return(disp_sentence)

            