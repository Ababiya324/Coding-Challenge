"""
Iron Man Air Canvas - Hand Gesture Drawing Application
Uses MediaPipe for hand tracking and OpenCV for visualization
Designed for Google Colab with webcam support
"""

import cv2
import mediapipe as mp
import numpy as np
from google.colab.patches import cv2_imshow
from IPython.display import display, Javascript, clear_output
from google.colab.output import eval_js
from base64 import b64decode
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Canvas settings
canvas = None
prev_x, prev_y = None, None
mode = "STANDBY"
draw_color = (255, 100, 0)  # Iron Man blue (BGR)
brush_thickness = 5

def take_photo(filename='photo.jpg', quality=0.8):
    """Capture image from webcam in Colab"""
    js = Javascript('''
        async function takePhoto(quality) {
            const div = document.createElement('div');
            const capture = document.createElement('button');
            capture.textContent = 'Capture';
            div.appendChild(capture);

            const video = document.createElement('video');
            video.style.display = 'block';
            const stream = await navigator.mediaDevices.getUserMedia({video: true});

            document.body.appendChild(div);
            div.appendChild(video);
            video.srcObject = stream;
            await video.play();

            // Resize video to fit
            google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

            // Wait for capture click
            await new Promise((resolve) => capture.onclick = resolve);

            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getVideoTracks()[0].stop();
            div.remove();
            return canvas.toDataURL('image/jpeg', quality);
        }
    ''')
    display(js)
    data = eval_js('takePhoto({})'.format(quality))
    binary = b64decode(data.split(',')[1])
    with open(filename, 'wb') as f:
        f.write(binary)
    return filename

def count_fingers(hand_landmarks):
    """Count extended fingers"""
    # Thumb, Index, Middle, Ring, Pinky tip landmarks
    finger_tips = [4, 8, 12, 16, 20]
    finger_pips = [3, 6, 10, 14, 18]

    count = 0

    # Thumb (special case - check horizontal distance)
    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_pips[0]].x:
        count += 1

    # Other fingers (check if tip is above pip)
    for i in range(1, 5):
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_pips[i]].y:
            count += 1

    return count

def detect_gesture(hand_landmarks):
    """Detect hand gesture based on finger count"""
    fingers = count_fingers(hand_landmarks)

    if fingers == 0:
        return "DRAW"  # Fist
    elif fingers == 1:
        return "DRAW"  # Index finger
    elif fingers == 2:
        return "ERASE"
    elif fingers >= 4:
        return "CLEAR"
    else:
        return "PAUSE"  # 3 fingers or open hand

def draw_hud(frame, mode, fps=0):
    """Draw Iron Man style HUD overlay"""
    height, width = frame.shape[:2]

    # HUD color (cyan/blue)
    hud_color = (255, 200, 0)
    text_color = (0, 255, 255)

    # Corner brackets
    bracket_size = 30
    bracket_thickness = 2

    # Top-left
    cv2.line(frame, (10, 10), (10 + bracket_size, 10), hud_color, bracket_thickness)
    cv2.line(frame, (10, 10), (10, 10 + bracket_size), hud_color, bracket_thickness)

    # Top-right
    cv2.line(frame, (width - 10, 10), (width - 10 - bracket_size, 10), hud_color, bracket_thickness)
    cv2.line(frame, (width - 10, 10), (width - 10, 10 + bracket_size), hud_color, bracket_thickness)

    # Bottom-left
    cv2.line(frame, (10, height - 10), (10 + bracket_size, height - 10), hud_color, bracket_thickness)
    cv2.line(frame, (10, height - 10), (10, height - 10 - bracket_size), hud_color, bracket_thickness)

    # Bottom-right
    cv2.line(frame, (width - 10, height - 10), (width - 10 - bracket_size, height - 10), hud_color, bracket_thickness)
    cv2.line(frame, (width - 10, height - 10), (width - 10, height - 10 - bracket_size), hud_color, bracket_thickness)

    # Mode indicator
    cv2.putText(frame, f"MODE: {mode}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

    # FPS counter
    cv2.putText(frame, f"FPS: {int(fps)}", (20, height - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_color, 1)

    # Instructions
    instructions = [
        "FIST/1 FINGER: DRAW",
        "2 FINGERS: ERASE",
        "5 FINGERS: CLEAR",
        "3+ FINGERS: PAUSE"
    ]

    y_offset = 50
    for i, instruction in enumerate(instructions):
        cv2.putText(frame, instruction, (width - 250, y_offset + i * 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, hud_color, 1)

    return frame

def draw_crosshair(frame, x, y, color=(0, 255, 255)):
    """Draw Iron Man style targeting crosshair"""
    size = 20
    thickness = 2

    # Horizontal line
    cv2.line(frame, (x - size, y), (x + size, y), color, thickness)
    # Vertical line
    cv2.line(frame, (x, y - size), (x, y + size), color, thickness)
    # Circle
    cv2.circle(frame, (x, y), size, color, thickness)
    cv2.circle(frame, (x, y), 3, color, -1)

def main():
    """Main application loop"""
    global canvas, prev_x, prev_y, mode

    print("🦾 IRON MAN AIR CANVAS - INITIALIZING...")
    print("📸 Click 'Capture' to start drawing!")
    print("\n⚡ CONTROLS:")
    print("  • Fist/1 Finger = Draw")
    print("  • 2 Fingers = Erase")
    print("  • 5 Fingers = Clear canvas")
    print("  • 3+ Fingers = Pause")
    print("\nPress 'q' to quit")

    # Capture single frame for processing
    frame_count = 0
    fps_start_time = time.time()
    fps = 0

    try:
        while True:
            # Capture frame from webcam
            filename = take_photo(quality=0.8)
            frame = cv2.imread(filename)

            if frame is None:
                print("❌ Failed to capture frame")
                break

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            height, width = frame.shape[:2]

            # Initialize canvas if needed
            if canvas is None:
                canvas = np.zeros((height, width, 3), dtype=np.uint8)

            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand skeleton
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 200, 0), thickness=2)
                    )

                    # Get index finger tip position
                    index_tip = hand_landmarks.landmark[8]
                    x = int(index_tip.x * width)
                    y = int(index_tip.y * height)

                    # Detect gesture
                    current_mode = detect_gesture(hand_landmarks)
                    mode = current_mode

                    # Draw crosshair at finger position
                    draw_crosshair(frame, x, y)

                    # Handle different modes
                    if mode == "DRAW":
                        if prev_x is not None and prev_y is not None:
                            # Draw line on canvas
                            cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, brush_thickness)
                        prev_x, prev_y = x, y

                    elif mode == "ERASE":
                        # Erase by drawing black circle
                        cv2.circle(canvas, (x, y), 20, (0, 0, 0), -1)
                        prev_x, prev_y = None, None

                    elif mode == "CLEAR":
                        # Clear entire canvas
                        canvas = np.zeros((height, width, 3), dtype=np.uint8)
                        prev_x, prev_y = None, None

                    elif mode == "PAUSE":
                        prev_x, prev_y = None, None
            else:
                mode = "STANDBY"
                prev_x, prev_y = None, None

            # Merge canvas with frame
            frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

            # Calculate FPS
            frame_count += 1
            if frame_count % 10 == 0:
                fps = 10 / (time.time() - fps_start_time)
                fps_start_time = time.time()

            # Draw HUD
            frame = draw_hud(frame, mode, fps)

            # Display frame
            clear_output(wait=True)
            cv2_imshow(frame)

            # Check for quit (in Colab, this will be manual interruption)
            print("\n🛑 To stop, interrupt the cell execution")

            # Small delay
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n✅ Air Canvas stopped")
    finally:
        hands.close()
        print("🦾 JARVIS offline")

if __name__ == "__main__":
    main()
