# Coding Challenge - Interactive Algorithms Website

An interactive web application showcasing three classic algorithms with beautiful UI and real-time results.

## 🌟 Features

### 1. Tower of Hanoi 🗼
- Recursive algorithm to solve the classic Tower of Hanoi puzzle
- Input: Number of disks (1-10)
- Output: Step-by-step solution showing all moves

### 2. Longest Increasing Subsequence 📈
- Dynamic programming solution to find LIS length
- Input: Comma-separated array of numbers
- Output: Length of the longest increasing subsequence

### 3. Roman to Integer Converter 🏛️
- Converts Roman numerals to integer values
- Input: Roman numeral string (e.g., MCMXCIV)
- Output: Integer equivalent (e.g., 1994)

## 🚀 How to Use

Simply open `index.html` in any modern web browser:

```bash
# Open in default browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

Or use a local server:

```bash
# Python 3
python -m http.server 8000

# Then visit http://localhost:8000
```

## 🎨 Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive UI**: Real-time algorithm execution
- **Beautiful Animations**: Smooth transitions and effects
- **Input Validation**: Prevents invalid inputs
- **Keyboard Support**: Press Enter to execute

## 📁 Project Structure

```
Coding-Challenge/
├── index.html          # Main website (HTML + CSS + JavaScript)
├── hanoi_tower.py      # Original Python implementation
├── length_of_lis.py    # Original Python implementation
├── roman_to_int.py     # Original Python implementation
├── README.md           # This file
└── LICENSE             # License information
```

## 🛠️ Technologies Used

- **HTML5**: Structure and content
- **CSS3**: Styling with gradients and animations
- **Vanilla JavaScript**: Algorithm implementation and interactivity
- **No dependencies**: Pure web technologies, no frameworks needed

## 💡 Algorithm Complexity

- **Tower of Hanoi**: O(2^n) time, O(n) space
- **LIS**: O(n²) time, O(n) space
- **Roman to Integer**: O(n) time, O(1) space

## 🤝 Contributing

Feel free to fork this repository and submit pull requests!

## 📄 License

See LICENSE file for details.
