# 🦾 Iron Man Air Canvas

An interactive hand-gesture controlled drawing application inspired by Iron Man's HUD interface. Uses MediaPipe for hand tracking and OpenCV for visualization.

## ✨ Features

- **Real-time Hand Tracking**: Uses MediaPipe to detect hand landmarks
- **Gesture Controls**:
  - ✊ **Fist/1 Finger**: Draw blue trail
  - ✌️ **2 Fingers**: Erase
  - 🖐️ **5 Fingers**: Clear entire canvas
  - ✋ **3-4 Fingers**: Pause drawing
- **Iron Man HUD**: Complete with crosshairs, corner brackets, and mode indicators
- **Visual Feedback**: Real-time hand skeleton overlay with targeting system

## 🚀 Quick Start (Google Colab)

### Step 1: Install MediaPipe

```python
!pip install mediapipe
```

### Step 2: Test Imports

```python
import cv2
import mediapipe as mp
import numpy as np
print("✅ ALL LIBRARIES READY!")
```

### Step 3: Run the Application

Copy the entire contents of `iron_man_canvas_single_cell.py` into a Colab cell and run!

Or simply run:

```python
# Upload the file to Colab, then:
%run iron_man_canvas_single_cell.py
```

## 📋 Files Included

1. **iron_man_canvas_single_cell.py** ⭐ RECOMMENDED
   - Complete single-cell implementation
   - Optimized for Google Colab
   - Object-oriented design
   - Easy to customize

2. **iron_man_air_canvas_colab.py**
   - Streamlined procedural version
   - Good for quick modifications
   - Inline implementation

3. **iron_man_air_canvas.py**
   - Original detailed implementation
   - Good for learning the concepts
   - More modular structure

## 🎮 How to Use

1. **Position your hand** in front of the webcam
2. **Make gestures** to control drawing:
   - Close your fist or point with index finger to draw
   - Show 2 fingers to erase
   - Show all 5 fingers to clear the canvas
   - Show 3-4 fingers to pause
3. **Watch the HUD** for current mode indicator

## ⚙️ Customization

### Change Draw Color
```python
self.draw_color = (255, 100, 0)  # BGR format
# Red: (0, 0, 255)
# Green: (0, 255, 0)
# Blue: (255, 0, 0)
# Purple: (255, 0, 255)
```

### Adjust Brush Thickness
```python
self.brush_thickness = 5  # Pixels
```

### Change Number of Frames
```python
canvas.run(num_frames=100)  # Process 100 frames
```

### Adjust Detection Sensitivity
```python
self.hands = self.mp_hands.Hands(
    min_detection_confidence=0.7,  # Lower = more sensitive
    min_tracking_confidence=0.5    # Lower = more sensitive
)
```

## 🔧 Technical Details

### Requirements
- Python 3.7+
- opencv-python (pre-installed in Colab)
- mediapipe
- numpy (pre-installed in Colab)

### How It Works
1. **Frame Capture**: Uses JavaScript to access webcam in Colab
2. **Hand Detection**: MediaPipe detects 21 hand landmarks
3. **Gesture Recognition**: Counts extended fingers to determine gesture
4. **Canvas Drawing**: Maintains separate canvas layer for persistence
5. **Overlay Rendering**: Combines camera feed with canvas and HUD

### Performance Tips
- Run in good lighting conditions
- Keep hand clearly visible to camera
- Avoid cluttered backgrounds
- Use steady hand movements for smooth drawing

## 🐛 Troubleshooting

**No hand detected?**
- Ensure good lighting
- Move hand closer to camera
- Check webcam permissions
- Lower detection confidence threshold

**Drawing not smooth?**
- Reduce frame processing delay
- Ensure stable internet connection
- Close other resource-intensive tabs

**Webcam not working?**
- Grant camera permissions when prompted
- Refresh page and try again
- Check browser compatibility (Chrome recommended)

## 📝 License

MIT License - Feel free to modify and use!

## 🎨 Created By

Built with ❤️ using MediaPipe and OpenCV
Inspired by Iron Man's J.A.R.V.I.S. interface

---

**"Sometimes you gotta run before you can walk."** - Tony Stark
