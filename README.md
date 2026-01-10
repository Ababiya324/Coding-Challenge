# Coding-Challenge

## Iron Man Air Canvas 🦾✨

An interactive hand-tracking drawing application that lets you draw in the air using your webcam! Featuring Iron Man-style HUD and visual effects.

### 🎨 Features

- **Real-time hand tracking** using MediaPipe and OpenCV
- **Gesture-based controls**:
  - ✊ **Fist** = Drawing mode (draw with your index fingertip)
  - ✋ **Open palm** = Move mode (move without drawing)
  - ✌️ **Two fingers** = Eraser mode
  - 🤚 **Five fingers** = Clear entire canvas
- **Iron Man HUD styling**:
  - Cyan/blue glowing drawing trails (like repulsor beams)
  - Targeting crosshair that follows your fingertip
  - Mode indicators with glow effects
  - Scanline and grid overlay effects
  - Real-time FPS counter
- **Save your drawings** as PNG images
- **Smooth performance** with gesture smoothing and optimized rendering

### 🚀 Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Coding-Challenge
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 📖 Usage

Run the application:
```bash
python iron_man_air_canvas.py
```

**Keyboard Controls:**
- `s` - Save your drawing as a PNG file
- `c` - Clear the canvas
- `q` - Quit the application

**Hand Gestures:**
1. Make sure your hand is visible to the webcam
2. Use different hand gestures to control the drawing mode
3. Point with your index finger to draw or navigate
4. The crosshair follows your index fingertip

### 💡 Tips for Best Results

- Ensure good lighting for better hand tracking
- Keep your hand clearly visible to the camera
- Make distinct gestures for more reliable detection
- The application works best with a plain background
- You can write equations, draw diagrams, or create art!

### 🛠️ Technical Details

**Technologies:**
- Python 3.x
- OpenCV (cv2) - Computer vision and video capture
- MediaPipe - Hand tracking and landmark detection
- NumPy - Image processing and array operations

**How it works:**
1. Captures video from your webcam in real-time
2. Uses MediaPipe Hands to detect hand landmarks
3. Analyzes finger positions to recognize gestures
4. Tracks index fingertip position for cursor location
5. Draws on a transparent canvas overlay with glow effects
6. Renders Iron Man-style HUD elements

### 📸 Example Use Cases

- Write mathematical equations in the air
- Draw diagrams for presentations
- Create digital art without touching anything
- Interactive teaching and demonstrations
- Fun party trick to impress your friends!

### 🎮 Project Structure

```
Coding-Challenge/
├── iron_man_air_canvas.py  # Main application
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── iron_man_drawing_*.png  # Saved drawings (generated)
```

### 🤝 Contributing

Feel free to fork this project and add your own features! Some ideas:
- Multiple color options with gesture controls
- Line thickness adjustment
- Undo/redo functionality
- Different brush styles
- Two-hand support for advanced controls

### 📝 License

See LICENSE file for details.

---

**Enjoy drawing in the air like Iron Man! 🦾✨**