#!/usr/bin/env python3
"""
Iron Man Air Canvas - Hand Tracking Drawing Application
Draw in the air using hand gestures with Iron Man HUD styling!

Gestures:
- ✊ Fist = Drawing mode (draw with fingertip)
- ✋ Open palm = Move mode (move without drawing)
- ✌️ Two fingers up = Eraser mode
- 🤚 All five fingers = Clear entire canvas

Controls:
- Press 's' to save your drawing
- Press 'c' to clear canvas
- Press 'q' to quit
"""

import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import time
import math

class IronManAirCanvas:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Webcam setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Get actual frame dimensions
        ret, frame = self.cap.read()
        if ret:
            self.frame_height, self.frame_width = frame.shape[:2]
        else:
            self.frame_height, self.frame_width = 720, 1280

        # Canvas for drawing
        self.canvas = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.uint8)

        # Drawing settings
        self.drawing_color = (255, 200, 0)  # Cyan/blue for Iron Man style
        self.drawing_thickness = 5
        self.eraser_size = 30

        # Mode tracking
        self.mode = "MOVE"  # DRAW, MOVE, ERASE, CLEAR
        self.prev_x, self.prev_y = None, None

        # Gesture history for smoothing
        self.gesture_history = deque(maxlen=5)

        # FPS tracking
        self.prev_time = time.time()
        self.fps = 0

        # Visual effects
        self.mode_change_time = 0
        self.scanline_offset = 0

    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def count_extended_fingers(self, landmarks):
        """Count how many fingers are extended."""
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        thumb_tip = 4

        extended_fingers = 0

        # Check thumb (different logic due to thumb orientation)
        thumb_tip_x = landmarks[thumb_tip].x
        thumb_ip_x = landmarks[thumb_tip - 1].x
        if abs(thumb_tip_x - thumb_ip_x) > 0.05:  # Threshold for thumb extension
            extended_fingers += 1

        # Check other fingers
        for tip_id in finger_tips:
            tip_y = landmarks[tip_id].y
            pip_y = landmarks[tip_id - 2].y  # PIP joint

            # If fingertip is above PIP joint, finger is extended
            if tip_y < pip_y:
                extended_fingers += 1

        return extended_fingers

    def detect_gesture(self, landmarks):
        """Detect hand gesture based on finger positions."""
        extended_fingers = self.count_extended_fingers(landmarks)

        # Check for fist (0 or 1 fingers extended)
        if extended_fingers <= 1:
            return "FIST"

        # Check for two fingers (peace sign)
        elif extended_fingers == 2:
            # Verify it's index and middle finger
            index_tip_y = landmarks[8].y
            middle_tip_y = landmarks[12].y
            ring_tip_y = landmarks[16].y

            if index_tip_y < landmarks[6].y and middle_tip_y < landmarks[10].y and ring_tip_y > landmarks[14].y:
                return "TWO_FINGERS"

        # Check for all five fingers extended
        elif extended_fingers >= 4:
            return "FIVE_FINGERS"

        # Open palm (3 or more fingers extended)
        else:
            return "OPEN_PALM"

    def get_fingertip_position(self, landmarks):
        """Get the index fingertip position in pixel coordinates."""
        index_tip = landmarks[8]
        x = int(index_tip.x * self.frame_width)
        y = int(index_tip.y * self.frame_height)
        return x, y

    def draw_crosshair(self, frame, x, y, color=(0, 255, 255), size=30):
        """Draw Iron Man style targeting crosshair."""
        # Center circle
        cv2.circle(frame, (x, y), 5, color, 2)
        cv2.circle(frame, (x, y), 15, color, 1)

        # Cross lines
        cv2.line(frame, (x - size, y), (x - 10, y), color, 2)
        cv2.line(frame, (x + 10, y), (x + size, y), color, 2)
        cv2.line(frame, (x, y - size), (x, y - 10), color, 2)
        cv2.line(frame, (x, y + 10), (x, y + size), color, 2)

        # Corner brackets
        bracket_size = 20
        bracket_offset = 25
        # Top-left
        cv2.line(frame, (x - bracket_offset, y - bracket_offset),
                (x - bracket_offset + bracket_size, y - bracket_offset), color, 2)
        cv2.line(frame, (x - bracket_offset, y - bracket_offset),
                (x - bracket_offset, y - bracket_offset + bracket_size), color, 2)
        # Top-right
        cv2.line(frame, (x + bracket_offset, y - bracket_offset),
                (x + bracket_offset - bracket_size, y - bracket_offset), color, 2)
        cv2.line(frame, (x + bracket_offset, y - bracket_offset),
                (x + bracket_offset, y - bracket_offset + bracket_size), color, 2)
        # Bottom-left
        cv2.line(frame, (x - bracket_offset, y + bracket_offset),
                (x - bracket_offset + bracket_size, y + bracket_offset), color, 2)
        cv2.line(frame, (x - bracket_offset, y + bracket_offset),
                (x - bracket_offset, y + bracket_offset - bracket_size), color, 2)
        # Bottom-right
        cv2.line(frame, (x + bracket_offset, y + bracket_offset),
                (x + bracket_offset - bracket_size, y + bracket_offset), color, 2)
        cv2.line(frame, (x + bracket_offset, y + bracket_offset),
                (x + bracket_offset, y + bracket_offset - bracket_size), color, 2)

    def draw_hud(self, frame):
        """Draw Iron Man style HUD overlay."""
        # Mode indicator
        mode_colors = {
            "DRAW": (0, 255, 255),      # Cyan
            "MOVE": (255, 255, 255),    # White
            "ERASE": (0, 0, 255),       # Red
            "CLEAR": (0, 255, 0)        # Green
        }

        mode_color = mode_colors.get(self.mode, (255, 255, 255))

        # Mode text with glow effect
        mode_text = f">>> {self.mode} MODE <<<"

        # Add glow effect
        for offset in range(5, 0, -1):
            alpha = 0.3 / offset
            glow_color = tuple(int(c * alpha) for c in mode_color)
            cv2.putText(frame, mode_text, (20, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, glow_color, offset + 2)

        # Main text
        cv2.putText(frame, mode_text, (20, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, mode_color, 3)

        # FPS counter
        cv2.putText(frame, f"FPS: {int(self.fps)}", (self.frame_width - 150, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Instructions panel
        instructions = [
            "GESTURE CONTROLS:",
            "Fist - DRAW MODE",
            "Open Palm - MOVE MODE",
            "Two Fingers - ERASE MODE",
            "Five Fingers - CLEAR ALL",
            "",
            "KEYS: [S]ave [C]lear [Q]uit"
        ]

        y_offset = self.frame_height - 200
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (20, y_offset + i * 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)

        # Scanline effect
        for i in range(0, self.frame_height, 4):
            y_pos = (i + self.scanline_offset) % self.frame_height
            cv2.line(frame, (0, y_pos), (self.frame_width, y_pos), (0, 50, 50), 1)

        self.scanline_offset = (self.scanline_offset + 2) % self.frame_height

        # Grid overlay (subtle)
        grid_spacing = 50
        grid_color = (0, 40, 40)
        for i in range(0, self.frame_width, grid_spacing):
            cv2.line(frame, (i, 0), (i, self.frame_height), grid_color, 1)
        for i in range(0, self.frame_height, grid_spacing):
            cv2.line(frame, (0, i), (self.frame_width, i), grid_color, 1)

        # Mode change flash effect
        if time.time() - self.mode_change_time < 0.5:
            alpha = 1.0 - (time.time() - self.mode_change_time) * 2
            overlay = np.zeros_like(frame)
            overlay[:, :] = mode_color
            cv2.addWeighted(frame, 1, overlay, alpha * 0.3, 0, frame)

    def process_drawing(self, x, y):
        """Process drawing based on current mode."""
        if self.mode == "DRAW":
            if self.prev_x is not None and self.prev_y is not None:
                # Draw glowing line
                # Create glow effect with multiple lines
                for thickness in range(self.drawing_thickness + 10, self.drawing_thickness, -2):
                    alpha = 0.3 / (thickness - self.drawing_thickness + 1)
                    glow_color = tuple(int(c * alpha) for c in self.drawing_color)
                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y),
                            glow_color, thickness, cv2.LINE_AA)

                # Main drawing line
                cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y),
                        self.drawing_color, self.drawing_thickness, cv2.LINE_AA)

            self.prev_x, self.prev_y = x, y

        elif self.mode == "ERASE":
            cv2.circle(self.canvas, (x, y), self.eraser_size, (0, 0, 0), -1)
            self.prev_x, self.prev_y = x, y

        elif self.mode == "MOVE":
            self.prev_x, self.prev_y = None, None

        elif self.mode == "CLEAR":
            self.canvas = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.uint8)
            self.mode = "MOVE"
            self.mode_change_time = time.time()

    def update_mode(self, gesture):
        """Update mode based on detected gesture."""
        new_mode = self.mode

        if gesture == "FIST":
            new_mode = "DRAW"
        elif gesture == "OPEN_PALM":
            new_mode = "MOVE"
        elif gesture == "TWO_FINGERS":
            new_mode = "ERASE"
        elif gesture == "FIVE_FINGERS":
            new_mode = "CLEAR"

        if new_mode != self.mode:
            self.mode = new_mode
            self.mode_change_time = time.time()
            self.prev_x, self.prev_y = None, None

    def save_canvas(self):
        """Save the current canvas to a file."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"iron_man_drawing_{timestamp}.png"
        cv2.imwrite(filename, self.canvas)
        print(f"Drawing saved as {filename}")

    def run(self):
        """Main application loop."""
        print("Iron Man Air Canvas Started!")
        print("Show your hand to the camera and use gestures to draw.")
        print("\nControls:")
        print("  ✊ Fist = Drawing mode")
        print("  ✋ Open palm = Move mode")
        print("  ✌️ Two fingers = Eraser mode")
        print("  🤚 Five fingers = Clear canvas")
        print("\nKeyboard:")
        print("  's' = Save drawing")
        print("  'c' = Clear canvas")
        print("  'q' = Quit")
        print("\n" + "="*50 + "\n")

        while True:
            success, frame = self.cap.read()
            if not success:
                print("Failed to read from camera")
                break

            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)

            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks (subtle)
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 100, 100), thickness=1),
                        self.mp_draw.DrawingSpec(color=(0, 150, 150), thickness=1)
                    )

                    # Get fingertip position
                    x, y = self.get_fingertip_position(hand_landmarks.landmark)

                    # Detect gesture
                    gesture = self.detect_gesture(hand_landmarks.landmark)
                    self.gesture_history.append(gesture)

                    # Smooth gesture detection
                    if len(self.gesture_history) >= 3:
                        most_common_gesture = max(set(self.gesture_history),
                                                 key=self.gesture_history.count)
                        self.update_mode(most_common_gesture)

                    # Process drawing
                    self.process_drawing(x, y)

                    # Draw crosshair
                    crosshair_color = {
                        "DRAW": (0, 255, 255),
                        "MOVE": (255, 255, 255),
                        "ERASE": (0, 0, 255),
                        "CLEAR": (0, 255, 0)
                    }.get(self.mode, (0, 255, 255))

                    self.draw_crosshair(frame, x, y, crosshair_color)
            else:
                self.prev_x, self.prev_y = None, None

            # Merge canvas with frame
            # Apply glow effect to canvas
            canvas_glow = cv2.GaussianBlur(self.canvas, (15, 15), 0)
            canvas_combined = cv2.addWeighted(self.canvas, 0.8, canvas_glow, 0.2, 0)

            # Combine frame and canvas
            frame = cv2.addWeighted(frame, 1, canvas_combined, 0.7, 0)

            # Draw HUD
            self.draw_hud(frame)

            # Calculate FPS
            current_time = time.time()
            self.fps = 1 / (current_time - self.prev_time)
            self.prev_time = current_time

            # Display
            cv2.imshow('Iron Man Air Canvas', frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.save_canvas()
            elif key == ord('c'):
                self.canvas = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.uint8)
                print("Canvas cleared")

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()

def main():
    """Main entry point."""
    try:
        app = IronManAirCanvas()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
