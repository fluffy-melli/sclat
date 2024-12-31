import math, cv2, sys, numpy as np, mediapipe as mp
from setting import setting as user_setting
import locale

if user_setting.Gesture:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        system_lang = locale.getdefaultlocale()[0]
        if system_lang and system_lang.startswith('ko'):
            error_msg = "제스쳐 인식을 위한 카메라를 찾을 수 없습니다.\n카메라를 연결한 후 다시 시도해주세요."
        else:
            error_msg = "Cannot find camera for gesture recognition.\nPlease connect a camera and try again."
        print(error_msg)
        sys.exit(1)

    hands = mp.solutions.hands.Hands(max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    pause = False

def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))

def run(vid):
    """
    Detect hand gestures for media control:
    - A closed fist (all fingers down) pauses the video
    - A specific gesture(Ok sign) with thumb and index finger together allows seeking through the video

    Parameters:
        end (int): The total duration of the media being controlled
    Returns:
        None
    Note:
        This feature displays the processed video feed in a window titled “Gesture Recognition”. 
        You can modify the settings for this in setting.json.
        
        Starting with mediapipe 0.10.18, 
        the console shows unnecessary logs that are unable to be removed. 
        I tried to configure it so that it doesn't appear, but was not successful...
        It would be nice if someone could do a fix to remove these logs.
    """
    global cap, pause
    res, frame = cap.read()

    end = int(vid.duration)
    
    if not res:
        print("Camera error")

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    hand_shape = ""
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp.solutions.hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style(),
        )
        
        points = hand_landmarks.landmark
        
        fingers = [0, 0, 0, 0, 0]
        
        if distance(points[4], points[9]) > distance(points[3], points[9]):
            fingers[0] = 1
        
        for i in range(1, 5):
            if distance(points[4 * (i + 1)], points[0]) > distance(points[4 * (i + 1) - 1], points[0]):
                fingers[i] = 1
        
        if fingers == [0, 0, 0, 0, 0]:
            hand_shape = "Stop"
            vid.pause()
            pause = True
        elif distance(points[4], points[8]) < 0.1 and fingers[2:] == [1, 1, 1]:
            pos = int(np.interp(points[8].x * w, (50, w - 50), (1, end - 1)))
            seekpos = end - (end - pos)
            vid.seek(seekpos, False)
            hand_shape = "Move"
        
        cv2.putText(
            frame,
            hand_shape,
            (int(points[12].x * frame.shape[1]), int(points[12].y * frame.shape[0])),
            cv2.FONT_HERSHEY_COMPLEX,
            3,
            (0, 255, 0),
            5,
        )
    
    if pause != False and hand_shape != "Stop" and vid.get_pos() != end:
        vid.resume()
    if user_setting.Gesture_show:
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height
        target_width = 320
        target_height = int(target_width / aspect_ratio)
        resized_frame = cv2.resize(frame, (target_width, target_height))
        cv2.imshow("Gesture Recognition", resized_frame)
        cv2.moveWindow("Gesture Recognition", 0, 0)

def close():
    cv2.destroyAllWindows()
    cap.release()