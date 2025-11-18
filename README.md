# Language Identity Map - CMU-Q Multimodal Project

An interactive web application exploring linguistic identity, shame, and translanguaging experiences among multilingual students at Carnegie Mellon University Qatar.

## 🎓 Project Overview

This application visualizes the linguistic experiences of students in the Arabian Gulf, mapping moments of linguistic shame, pride, code-switching, and identity negotiation across CMU-Q's campus. Through an interactive map interface, users can explore real student stories and understand the complex relationship between language, space, and identity in institutional settings.

### Academic Context

The project draws on scholarly frameworks including:
- **Linguistic Shame** (Sara Hillman, 2019) - Emotional responses to perceived linguistic inadequacy
- **Translanguaging** (García & Wei) - Fluid use of multiple languages as a unified repertoire
- **Chronotope** (Blommaert) - How time and space shape language practices and identities
- **Enoughness** - Negotiating cultural and linguistic authenticity across contexts

## ✨ Features

### 🗺️ Interactive Campus Map
- Stylized SVG map of CMU-Q campus showing 6 key locations
- Clickable buildings and story dots
- Color-coded markers indicating experience types:
  - 🔴 Red: Linguistic Shame
  - 🟢 Green: Linguistic Pride
  - 🔵 Blue: Code-Switching
  - 🟡 Yellow: Identity Negotiation
- Animated story dots with pulse effects

### 📊 Statistics Dashboard
- Real-time statistics on stories, languages, and experiences
- Animated counters
- Responsive grid layout

### 🎯 Filtering System
- Filter by experience type (Shame, Pride, Code-Switching, Negotiation)
- Filter by language (Arabic, English, Multilingual)
- Filter by student background (Qatari, GCC National, International)
- Real-time map updates

### 📖 Story Modal
- Rich story display with student profiles
- Tagged metadata (location, languages, experience type)
- Academic concept explanations
- Navigation between stories at the same location
- Keyboard navigation support (Arrow keys, Escape)

### ✍️ Contribution Form
- Submit new linguistic experiences
- LocalStorage persistence for demo purposes
- Form validation
- Success feedback

### ♿ Accessibility Features
- ARIA labels for screen readers
- Keyboard navigation throughout
- Focus indicators on interactive elements
- WCAG AA color contrast compliance
- Reduced motion support for users with motion sensitivities

### 🌐 Multilingual Support
- Displays stories with translanguaging (mixed Arabic/English)
- Unicode support for Arabic script
- Right-to-left text rendering

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- No server or build tools required!

### Installation

1. **Clone or Download** this repository to your local machine

2. **Open the project**
   ```bash
   cd Coding-Challenge
   ```

3. **Launch the application**
   - Simply open `index.html` in your web browser
   - Or use a local server (optional):
     ```bash
     # Using Python 3
     python -m http.server 8000

     # Using PHP
     php -S localhost:8000

     # Using Node.js (http-server)
     npx http-server
     ```

4. **View in browser**
   - Navigate to `http://localhost:8000` (if using a server)
   - Or double-click `index.html` to open directly

## 📁 Project Structure

```
Coding-Challenge/
├── index.html              # Main HTML structure
├── css/
│   ├── styles.css          # Main styles with CMU colors
│   └── animations.css      # Animations and transitions
├── js/
│   ├── data.js             # Story data and campus locations
│   ├── map.js              # Map generation and interactions
│   └── main.js             # Filtering, forms, and UI logic
├── assets/                 # (Currently empty - for future images)
└── README.md               # This file
```

## 🎨 Design

### Color Scheme
- **Primary Red**: `#C41230` (CMU Red)
- **Dark Red**: `#A00F27`
- **Gray**: `#666666`
- **Light Gray**: `#F5F5F5`
- **Experience Colors**:
  - Shame: `#C41230` (Red)
  - Pride: `#28a745` (Green)
  - Code-Switching: `#007bff` (Blue)
  - Negotiation: `#ffc107` (Yellow)

### Typography
- Font Family: Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- Loaded from Google Fonts

### Responsive Breakpoints
- Desktop: > 768px
- Tablet: 481px - 768px
- Mobile: ≤ 480px

## 🔧 Technical Details

### Technologies Used
- **HTML5** - Semantic structure
- **CSS3** - Styling with Grid, Flexbox, and animations
- **Vanilla JavaScript (ES6+)** - No frameworks or libraries
- **SVG** - Interactive campus map
- **LocalStorage API** - Persist user contributions

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Performance
- Lightweight (< 100KB total)
- No external dependencies (except Google Fonts)
- Runs entirely offline after initial load

## 📚 Data Structure

Stories follow this JSON structure:

```javascript
{
  id: 1,
  location: "Academic Building",
  coordinates: { x: 35, y: 40 },
  studentProfile: "International Student from Ethiopia",
  languages: ["English", "Amharic"],
  experienceType: "Linguistic Shame",
  story: "Story text here...",
  academicConcept: "Linguistic Shame (Hillman, 2019)",
  timestamp: "2024-11-15"
}
```

### Current Dataset
- **20 pre-populated stories** covering diverse experiences
- Stories include students from 15+ countries
- 12+ languages represented
- All 6 campus locations covered

## 🎯 Usage Guide

### Exploring Stories
1. Click on any building or colored dot on the map
2. Read the student's story in the modal
3. Use arrow keys or buttons to navigate between stories
4. Press Escape to close the modal

### Filtering
1. Use dropdown menus above the map
2. Select experience type, language, or student background
3. Click "Reset Filters" to show all stories

### Contributing a Story
1. Scroll to the "Share Your Story" section
2. Fill in your experience (2-4 sentences recommended)
3. Select location and experience type
4. Add languages and optional background info
5. Submit - your story appears on the map instantly!

### Advanced Features
- Open browser console and type `printStatistics()` to see detailed breakdowns
- Type `exportStories()` to download all stories as JSON

## 🔮 Future Enhancements

### Potential Features
- [ ] Search functionality for keywords
- [ ] Heat map overlay showing concentration of experiences
- [ ] Timeline slider to filter by date
- [ ] Audio recordings of students telling their stories
- [ ] Backend integration for persistent storage
- [ ] Moderation system for user submissions
- [ ] Multilingual UI (Arabic interface option)
- [ ] Data visualization charts (pie charts, bar graphs)
- [ ] Integration with CMU-Q authentication
- [ ] Download stories as PDF report
- [ ] Social media sharing
- [ ] Comparison view between different locations
- [ ] Anonymous commenting on stories

### Technical Improvements
- [ ] Service worker for full offline support
- [ ] Progressive Web App (PWA) capabilities
- [ ] IndexedDB for more robust storage
- [ ] TypeScript migration
- [ ] Unit tests
- [ ] Accessibility audit and improvements
- [ ] Performance optimization with lazy loading

## 🧪 Testing

### Manual Testing Checklist
- [x] All interactive elements are clickable
- [x] Filters update the map correctly
- [x] Modal opens and closes smoothly
- [x] Form validation works
- [x] LocalStorage persists data
- [x] Responsive design works on mobile
- [x] Keyboard navigation functions
- [x] No console errors

### Test the Application
```bash
# No automated tests yet - manual testing recommended

# Test filters
1. Apply each filter type
2. Combine multiple filters
3. Reset filters

# Test form
1. Submit with missing fields (should fail)
2. Submit with all fields (should succeed)
3. Refresh page - submitted story should persist

# Test responsiveness
1. Resize browser window
2. Test on mobile device
3. Test on tablet
```

## 📖 Academic References

- Blommaert, J. (2015). Chronotopes, scales, and complexity in the study of language in society. *Annual Review of Anthropology*, 44, 105-116.
- García, O., & Wei, L. (2014). *Translanguaging: Language, bilingualism and education*. Palgrave Macmillan.
- Hillman, S. (2019). The language of loss: Translanguaging and linguistic shame among multilingual migrants. *Applied Linguistics Review*.

## 👥 Credits

**Created for**: CMU-Q Multimodal Project, Fall 2024
**Purpose**: Academic exploration of linguistic identity in the Arabian Gulf
**Institution**: Carnegie Mellon University Qatar

## 📄 License

This project is created for academic purposes. All student stories are anonymized to protect privacy.

## 🤝 Contributing

This is an academic project, but contributions are welcome:
- Report bugs via issues
- Suggest enhancements
- Share additional stories (anonymously)
- Improve documentation

## 📞 Support

For questions about the project or the research:
- Review the About section on the website
- Check academic references for theoretical background
- Explore the code comments for technical details

## ⚠️ Privacy Notice

All stories are anonymized. No personally identifying information is collected. In this demo version, user submissions are stored in browser LocalStorage only. In a production environment, all submissions would be reviewed before publication.

---

**Note**: This is a demonstration application. For production use, implement:
- Backend database
- User authentication
- Content moderation system
- HTTPS encryption
- Privacy policy and terms of service
