"""
Iron Man Air Canvas - Colab Edition
Complete single-cell implementation for Google Colab
Uses webcam streaming with MediaPipe hand tracking
"""

# === SINGLE CELL VERSION FOR COLAB ===

import cv2
import mediapipe as mp
import numpy as np
from google.colab.patches import cv2_imshow
from IPython.display import display, Javascript, clear_output
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import time
from io import BytesIO
from PIL import Image

print("🦾 IRON MAN AIR CANVAS - INITIALIZING JARVIS...")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Global variables
canvas = None
prev_x, prev_y = None, None
mode = "STANDBY"
draw_color = (255, 100, 0)  # Iron Man blue
brush_thickness = 5

def count_fingers(hand_landmarks):
    """Count extended fingers"""
    finger_tips = [4, 8, 12, 16, 20]
    finger_pips = [3, 6, 10, 14, 18]
    count = 0

    # Thumb
    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_pips[0]].x:
        count += 1

    # Other fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_pips[i]].y:
            count += 1

    return count

def detect_gesture(hand_landmarks):
    """Detect gesture from finger count"""
    fingers = count_fingers(hand_landmarks)
    if fingers == 0 or fingers == 1:
        return "DRAW"
    elif fingers == 2:
        return "ERASE"
    elif fingers >= 5:
        return "CLEAR"
    else:
        return "PAUSE"

def draw_hud(frame, mode, frame_count):
    """Draw Iron Man HUD overlay"""
    height, width = frame.shape[:2]
    hud_color = (255, 200, 0)
    text_color = (0, 255, 255)

    # Corner brackets
    size, thick = 30, 2
    cv2.line(frame, (10, 10), (40, 10), hud_color, thick)
    cv2.line(frame, (10, 10), (10, 40), hud_color, thick)
    cv2.line(frame, (width-10, 10), (width-40, 10), hud_color, thick)
    cv2.line(frame, (width-10, 10), (width-10, 40), hud_color, thick)
    cv2.line(frame, (10, height-10), (40, height-10), hud_color, thick)
    cv2.line(frame, (10, height-10), (10, height-40), hud_color, thick)
    cv2.line(frame, (width-10, height-10), (width-40, height-10), hud_color, thick)
    cv2.line(frame, (width-10, height-10), (width-10, height-40), hud_color, thick)

    # Mode display
    cv2.putText(frame, f"MODE: {mode}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
    cv2.putText(frame, f"FRAME: {frame_count}", (20, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_color, 1)

    # Instructions
    instructions = [
        "FIST/1: DRAW",
        "2 FINGERS: ERASE",
        "5 FINGERS: CLEAR",
        "3-4: PAUSE"
    ]
    for i, inst in enumerate(instructions):
        cv2.putText(frame, inst, (width-200, 50+i*25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, hud_color, 1)

    return frame

def draw_crosshair(frame, x, y, color=(0, 255, 255)):
    """Draw targeting crosshair"""
    size, thick = 20, 2
    cv2.line(frame, (x-size, y), (x+size, y), color, thick)
    cv2.line(frame, (x, y-size), (x, y+size), color, thick)
    cv2.circle(frame, (x, y), size, color, thick)
    cv2.circle(frame, (x, y), 3, color, -1)

def capture_frame():
    """Capture single frame from webcam"""
    js_code = Javascript('''
        async function captureFrame() {
            const video = document.createElement('video');
            const stream = await navigator.mediaDevices.getUserMedia({video: true});
            video.srcObject = stream;
            await video.play();

            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);

            stream.getTracks().forEach(track => track.stop());

            return canvas.toDataURL('image/jpeg', 0.8);
        }
    ''')
    display(js_code)
    data = eval_js('captureFrame()')
    binary = b64decode(data.split(',')[1])

    img = Image.open(BytesIO(binary))
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return frame

# Main loop
print("⚡ SYSTEM ONLINE")
print("📸 Initializing webcam stream...")
print("\n🎮 CONTROLS:")
print("  • Fist/1 Finger → Draw blue trail")
print("  • 2 Fingers → Erase")
print("  • 5 Fingers → Clear canvas")
print("  • 3-4 Fingers → Pause")
print("\n🛑 Interrupt cell to stop\n")

frame_count = 0

try:
    for i in range(100):  # Capture 100 frames (adjust as needed)
        # Capture frame
        frame = capture_frame()
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]

        # Initialize canvas
        if canvas is None:
            canvas = np.zeros((height, width, 3), dtype=np.uint8)

        # Process with MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Handle detections
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw skeleton
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 200, 0), thickness=2)
                )

                # Get finger position
                index_tip = hand_landmarks.landmark[8]
                x = int(index_tip.x * width)
                y = int(index_tip.y * height)

                # Detect gesture
                mode = detect_gesture(hand_landmarks)

                # Draw crosshair
                draw_crosshair(frame, x, y)

                # Execute gesture
                if mode == "DRAW":
                    if prev_x is not None:
                        cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, brush_thickness)
                    prev_x, prev_y = x, y
                elif mode == "ERASE":
                    cv2.circle(canvas, (x, y), 20, (0, 0, 0), -1)
                    prev_x, prev_y = None, None
                elif mode == "CLEAR":
                    canvas = np.zeros((height, width, 3), dtype=np.uint8)
                    prev_x, prev_y = None, None
                elif mode == "PAUSE":
                    prev_x, prev_y = None, None
        else:
            mode = "STANDBY"
            prev_x, prev_y = None, None

        # Merge canvas and frame
        output = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
        output = draw_hud(output, mode, frame_count)

        # Display
        clear_output(wait=True)
        cv2_imshow(output)
        print(f"🎯 Frame {frame_count} | Mode: {mode}")

        frame_count += 1
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n✅ Canvas session ended")
finally:
    hands.close()
    print("🦾 JARVIS offline")
