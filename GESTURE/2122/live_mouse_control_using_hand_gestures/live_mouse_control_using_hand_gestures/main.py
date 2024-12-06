import cv2
import mediapipe as mp
import pyautogui
import random
import util
from pynput.mouse import Button, Controller
mouse = Controller()
import collections


screen_width, screen_height = pyautogui.size()
hand_positions = collections.deque(maxlen=10)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def is_hello_gesture(landmark_list):
    if len(hand_positions) < hand_positions.maxlen:
        return False

    x_positions = [pos[0] for pos in hand_positions]
    if max(x_positions) - min(x_positions) > 0.1:  # Adjust this threshold as needed
        return True

    return False

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0] 
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None, None

def is_pointing_to_self(landmark_list):
    return (
        util.get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) < 30 and  # Thumb folded
        util.get_angle(landmark_list[6], landmark_list[7], landmark_list[8]) < 30  # Index finger pointing
    )

def is_name_sign(landmark_list):
    return (
        util.get_angle(landmark_list[10], landmark_list[11], landmark_list[12]) < 30 and  # Middle finger folded
        util.get_angle(landmark_list[14], landmark_list[15], landmark_list[16]) < 30  # Ring finger folded
    )

def is_what_is_your_name_gesture(landmark_list):
    if len(hand_positions) < hand_positions.maxlen:
        return False

    x_positions = [pos[0] for pos in hand_positions]
    y_positions = [pos[1] for pos in hand_positions]
    if max(x_positions) - min(x_positions) > 0.1 and max(y_positions) - min(y_positions) < 0.1:  # Adjust these thresholds as needed
        return is_pointing_to_self(landmark_list) and is_name_sign(landmark_list)

    return False


def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        pyautogui.moveTo(x, y)


def is_left_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            thumb_index_dist > 50
    )


def is_right_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90  and
            thumb_index_dist > 50
    )


def is_double_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist > 50
    )


def is_screenshot(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist < 50
    )

def is_scroll_up(landmark_list):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 160 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 160 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 160 and
        util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) > 160 and
        landmark_list[4][1] < landmark_list[8][1]  # Thumb above index finger
    )
def is_scroll_down(landmark_list):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 160 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 160 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 160 and
        util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) > 160 and
        landmark_list[4][1] > landmark_list[8][1]  # Thumb below index finger
    )
def is_zoom_in(landmark_list):
    return (
        util.get_distance([landmark_list[4], landmark_list[8]]) < 40 and
        util.get_distance([landmark_list[4], landmark_list[12]]) > 50 and
        util.get_distance([landmark_list[8], landmark_list[12]]) > 50
    )
def is_zoom_out(landmark_list):
    return (
        util.get_distance([landmark_list[4], landmark_list[8]]) > 80 and
        util.get_distance([landmark_list[8], landmark_list[12]]) > 80 and
        util.get_distance([landmark_list[4], landmark_list[12]]) > 80
    )

#isi function code

def is_letter_a(landmark_list):
    return (
        util.get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) > 160 and  # Thumb extended
        util.get_angle(landmark_list[6], landmark_list[7], landmark_list[8]) < 30 and  # Index finger folded
        util.get_angle(landmark_list[10], landmark_list[11], landmark_list[12]) < 30 and  # Middle finger folded
        util.get_angle(landmark_list[14], landmark_list[15], landmark_list[16]) < 30 and  # Ring finger folded
        util.get_angle(landmark_list[18], landmark_list[19], landmark_list[20]) < 30  # Pinky finger -
    )

def is_letter_b(landmark_list):
    return (
        util.get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) < 30 and  # Thumb folded
        util.get_angle(landmark_list[6], landmark_list[7], landmark_list[8]) > 160 and  # Index finger extended
        util.get_angle(landmark_list[10], landmark_list[11], landmark_list[12]) > 160 and  # Middle finger extended
        util.get_angle(landmark_list[14], landmark_list[15], landmark_list[16]) > 160 and  # Ring finger extended
        util.get_angle(landmark_list[18], landmark_list[19], landmark_list[20]) > 160  # Pinky finger extended
    )
def is_letter_c(landmark_list):
    return (
        util.get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) > 30 and util.get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) < 160 and  # Thumb curved
        util.get_angle(landmark_list[6], landmark_list[7], landmark_list[8]) > 30 and util.get_angle(landmark_list[6], landmark_list[7], landmark_list[8]) < 160 and  # Index finger curved
        util.get_angle(landmark_list[10], landmark_list[11], landmark_list[12]) > 30 and util.get_angle(landmark_list[10], landmark_list[11], landmark_list[12]) < 160 and  # Middle finger curved
        util.get_angle(landmark_list[14], landmark_list[15], landmark_list[16]) > 30 and util.get_angle(landmark_list[14], landmark_list[15], landmark_list[16]) < 160 and  # Ring finger curved
        util.get_angle(landmark_list[18], landmark_list[19], landmark_list[20]) > 30 and util.get_angle(landmark_list[18], landmark_list[19], landmark_list[20]) < 160  # Pinky finger curved
    )

def is_letter_d(landmark_list):
    return (
        util.get_angle(landmark_list[2], landmark_list[3], landmark_list[4]) > 160 and  # Thumb extended
        util.get_angle(landmark_list[6], landmark_list[7], landmark_list[8]) > 160 and  # Index finger extended
        util.get_angle(landmark_list[10], landmark_list[11], landmark_list[12]) < 30 and  # Middle finger folded
        util.get_angle(landmark_list[14], landmark_list[15], landmark_list[16]) < 30 and  # Ring finger folded
        util.get_angle(landmark_list[18], landmark_list[19], landmark_list[20]) < 30  # Pinky finger folded
    )


def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:

        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if index_finger_tip:
            hand_positions.append((index_finger_tip.x, index_finger_tip.y))

        if is_what_is_your_name_gesture(landmark_list):
            cv2.putText(frame, "What is your name?", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif util.get_distance([landmark_list[4], landmark_list[5]]) < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        if is_hello_gesture(landmark_list):
            cv2.putText(frame, "Hello", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif util.get_distance([landmark_list[4], landmark_list[5]]) < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif is_left_click(landmark_list,  thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list, thumb_index_dist):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_scroll_up(landmark_list):
            pyautogui.scroll(5)
            cv2.putText(frame, "Scroll Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_scroll_down(landmark_list):
            pyautogui.scroll(-5)
            cv2.putText(frame, "Scroll Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_zoom_in(landmark_list):
            pyautogui.hotkey('ctrl', '+')
            cv2.putText(frame, "Zoom In", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_zoom_out(landmark_list):
            pyautogui.hotkey('ctrl', '-')
            cv2.putText(frame, "Zoom Out", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_letter_a(landmark_list):
            cv2.putText(frame, "Letter A", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_letter_b(landmark_list):
            cv2.putText(frame, "Letter B", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_letter_c(landmark_list):
            cv2.putText(frame, "Letter C", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_letter_d(landmark_list):
            cv2.putText(frame, "Letter D", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0] 
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
