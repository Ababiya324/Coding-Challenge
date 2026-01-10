"""
🦾 IRON MAN AIR CANVAS - Single Cell Edition
Copy this entire code into ONE Google Colab cell and run!

Requirements (pre-installed in Colab):
- opencv-python (cv2)
- mediapipe
- numpy

Additional install needed:
!pip install mediapipe
"""

import cv2
import mediapipe as mp
import numpy as np
from google.colab.patches import cv2_imshow
from IPython.display import display, Javascript, clear_output, Image as IPImage
from google.colab.output import eval_js
from base64 import b64decode
import time

class IronManCanvas:
    """Iron Man Air Canvas with hand gesture control"""

    def __init__(self):
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # Drawing state
        self.canvas = None
        self.prev_x = None
        self.prev_y = None
        self.mode = "STANDBY"
        self.draw_color = (255, 100, 0)  # Iron Man blue (BGR)
        self.brush_thickness = 5

        print("🦾 IRON MAN AIR CANVAS INITIALIZED")
        print("=" * 50)
        print("⚡ JARVIS ONLINE")
        print("=" * 50)
        print("\n🎮 GESTURE CONTROLS:")
        print("  ✊ Fist/1 Finger → DRAW (Blue Trail)")
        print("  ✌️  2 Fingers → ERASE")
        print("  🖐️  5 Fingers → CLEAR CANVAS")
        print("  ✋ 3-4 Fingers → PAUSE")
        print("\n🛑 Interrupt cell execution to stop")
        print("=" * 50 + "\n")

    def capture_webcam_frame(self):
        """Capture frame from webcam using JavaScript"""
        js = Javascript('''
            async function captureFrame() {
                const video = document.createElement('video');
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {width: 640, height: 480}
                });

                video.srcObject = stream;
                await video.play();

                // Wait for video to be ready
                await new Promise(resolve => setTimeout(resolve, 100));

                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);

                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());

                return canvas.toDataURL('image/jpeg', 0.8);
            }
        ''')

        display(js)
        data = eval_js('captureFrame()')

        # Decode image
        binary = b64decode(data.split(',')[1])

        # Convert to numpy array
        nparr = np.frombuffer(binary, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return frame

    def count_fingers(self, hand_landmarks):
        """Count number of extended fingers"""
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [3, 6, 10, 14, 18]

        count = 0

        # Thumb (check horizontal position)
        if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_pips[0]].x:
            count += 1

        # Other fingers (check if tip is above pip joint)
        for i in range(1, 5):
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_pips[i]].y:
                count += 1

        return count

    def detect_gesture(self, hand_landmarks):
        """Detect gesture based on finger count"""
        fingers = self.count_fingers(hand_landmarks)

        if fingers == 0 or fingers == 1:
            return "DRAW"  # Fist or pointing
        elif fingers == 2:
            return "ERASE"
        elif fingers >= 5:
            return "CLEAR"
        else:
            return "PAUSE"  # 3 or 4 fingers

    def draw_crosshair(self, frame, x, y, color=(0, 255, 255)):
        """Draw Iron Man targeting crosshair"""
        size = 20
        thickness = 2

        # Crosshair lines
        cv2.line(frame, (x - size, y), (x + size, y), color, thickness)
        cv2.line(frame, (x, y - size), (x, y + size), color, thickness)

        # Circles
        cv2.circle(frame, (x, y), size, color, thickness)
        cv2.circle(frame, (x, y), 3, color, -1)

    def draw_hud(self, frame, mode, frame_num):
        """Draw Iron Man HUD interface"""
        height, width = frame.shape[:2]

        hud_color = (255, 200, 0)  # Cyan/Blue
        text_color = (0, 255, 255)  # Yellow

        # Corner brackets
        bracket_size = 30
        thickness = 2

        # Top-left corner
        cv2.line(frame, (10, 10), (10 + bracket_size, 10), hud_color, thickness)
        cv2.line(frame, (10, 10), (10, 10 + bracket_size), hud_color, thickness)

        # Top-right corner
        cv2.line(frame, (width - 10, 10), (width - 10 - bracket_size, 10), hud_color, thickness)
        cv2.line(frame, (width - 10, 10), (width - 10, 10 + bracket_size), hud_color, thickness)

        # Bottom-left corner
        cv2.line(frame, (10, height - 10), (10 + bracket_size, height - 10), hud_color, thickness)
        cv2.line(frame, (10, height - 10), (10, height - 10 - bracket_size), hud_color, thickness)

        # Bottom-right corner
        cv2.line(frame, (width - 10, height - 10), (width - 10 - bracket_size, height - 10), hud_color, thickness)
        cv2.line(frame, (width - 10, height - 10), (width - 10, height - 10 - bracket_size), hud_color, thickness)

        # Mode indicator with status color
        mode_colors = {
            "DRAW": (0, 255, 0),
            "ERASE": (0, 165, 255),
            "CLEAR": (0, 0, 255),
            "PAUSE": (0, 255, 255),
            "STANDBY": (128, 128, 128)
        }
        mode_color = mode_colors.get(mode, text_color)

        cv2.putText(frame, f"MODE: {mode}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, mode_color, 2)

        # Frame counter
        cv2.putText(frame, f"FRAME: {frame_num:03d}", (20, height - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, hud_color, 1)

        # Control instructions
        instructions = [
            "FIST/1: DRAW",
            "2 FINGERS: ERASE",
            "5 FINGERS: CLEAR",
            "3-4: PAUSE"
        ]

        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (width - 200, 50 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, hud_color, 1)

        # JARVIS branding
        cv2.putText(frame, "JARVIS v2.0", (width - 150, height - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, hud_color, 1)

        return frame

    def process_frame(self, frame):
        """Process single frame with hand tracking and drawing"""
        # Flip for mirror effect
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]

        # Initialize canvas if needed
        if self.canvas is None:
            self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        # Process hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand skeleton
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(255, 200, 0), thickness=2)
                )

                # Get index fingertip position
                index_tip = hand_landmarks.landmark[8]
                x = int(index_tip.x * width)
                y = int(index_tip.y * height)

                # Detect gesture
                self.mode = self.detect_gesture(hand_landmarks)

                # Draw crosshair
                self.draw_crosshair(frame, x, y)

                # Execute gesture action
                if self.mode == "DRAW":
                    if self.prev_x is not None and self.prev_y is not None:
                        cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y),
                                self.draw_color, self.brush_thickness)
                    self.prev_x, self.prev_y = x, y

                elif self.mode == "ERASE":
                    cv2.circle(self.canvas, (x, y), 20, (0, 0, 0), -1)
                    self.prev_x, self.prev_y = None, None

                elif self.mode == "CLEAR":
                    self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
                    self.prev_x, self.prev_y = None, None

                elif self.mode == "PAUSE":
                    self.prev_x, self.prev_y = None, None
        else:
            self.mode = "STANDBY"
            self.prev_x, self.prev_y = None, None

        # Merge canvas with camera feed
        output = cv2.addWeighted(frame, 0.7, self.canvas, 0.3, 0)

        return output

    def run(self, num_frames=50):
        """Main loop - capture and process frames"""
        try:
            for frame_num in range(num_frames):
                # Capture frame
                frame = self.capture_webcam_frame()

                if frame is None:
                    print("❌ Failed to capture frame")
                    continue

                # Process frame
                output = self.process_frame(frame)

                # Draw HUD
                output = self.draw_hud(output, self.mode, frame_num)

                # Display
                clear_output(wait=True)
                cv2_imshow(output)
                print(f"🎯 Frame {frame_num + 1}/{num_frames} | Mode: {self.mode}")

                # Small delay
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\n✅ Session interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            self.hands.close()
            print("\n" + "=" * 50)
            print("🦾 JARVIS OFFLINE")
            print("=" * 50)

# Run the application
if __name__ == "__main__":
    canvas = IronManCanvas()
    canvas.run(num_frames=50)  # Adjust number of frames as needed

# To run again with more frames:
# canvas.run(num_frames=100)
