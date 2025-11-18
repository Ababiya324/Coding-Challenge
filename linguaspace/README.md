# LinguaSpace 🗣️

**Where Multilingual Voices Find Community**

A Reddit-style community forum exploring linguistic identity, translanguaging, and multilingual experiences among students at Carnegie Mellon University Qatar (CMU-Q).

![LinguaSpace Banner](https://img.shields.io/badge/Project-Linguistic_Identity-5865F2) ![Status](https://img.shields.io/badge/Status-Demo-2ECC71) ![License](https://img.shields.io/badge/License-Academic-FF6B6B)

---

## 📚 Table of Contents

- [About](#about)
- [Features](#features)
- [Academic Context](#academic-context)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Usage Guide](#usage-guide)
- [Data Persistence](#data-persistence)
- [Future Enhancements](#future-enhancements)
- [Credits](#credits)

---

## 🎯 About

LinguaSpace is an interactive web application designed for a university multimodal project about linguistic identity in the Arabian Gulf. It provides a safe, anonymous platform where multilingual students can:

- Share experiences with accent anxiety and code-switching
- Validate each other's struggles with linguistic identity
- Celebrate translanguaging and multilingual pride
- Build community around shared experiences

**Important**: This is a demo application for academic purposes. All data is stored locally in the browser using localStorage.

---

## ✨ Features

### Core Functionality

#### 📂 Six Community Categories
- **r/AccentAnxiety** - Stories about accent-related insecurity and judgment
- **r/CodeSwitchingStruggles** - The daily labor of switching between linguistic identities
- **r/TranslanguagingWins** - Celebrating moments of mixing languages successfully
- **r/NotEnoughTooMuch** - Feeling "not Arab enough" or "too foreign"
- **r/LanguagePolicing** - When others correct or police your language use
- **r/MultilingualPride** - Celebrating our multilingual identities

#### 🎨 Interactive Features
- **Upvote/Downvote System**: Reddit-style voting with localStorage persistence
- **Comment Threading**: Nested comments up to 3 levels deep
- **Advanced Filtering**: Filter by category, language, experience type
- **Live Search**: Real-time search across titles, content, and users
- **Multiple Sort Options**: Hot, New, Top (Week/Month/All Time)
- **Story Submission**: Anonymous story sharing with form validation

#### 🎭 Anonymous Participation
- Auto-generated anonymous usernames
- Safe space for sharing sensitive experiences
- No personal information required

#### 💾 Local Storage
- Vote history persistence
- Saved posts
- User-submitted stories
- First-visit detection

#### ♿ Accessibility
- ARIA labels throughout
- Keyboard navigation support
- Focus indicators
- Screen reader compatibility
- WCAG AA color contrast

#### 📱 Responsive Design
- Desktop, tablet, and mobile optimized
- Touch-friendly interactions
- Adaptive layouts
- Mobile-first approach

---

## 🎓 Academic Context

### Key Concepts

#### 💡 Linguistic Shame (Sara Hillman)
The feeling of inadequacy or embarrassment about one's language use, accent, or perceived language deficiency. Often experienced by multilingual individuals when navigating between linguistic communities.

#### 🌐 Translanguaging
The natural practice of multilingual speakers seamlessly moving between languages in communication. Rather than keeping languages separate, translanguaging recognizes the fluid, dynamic nature of multilingual expression.

#### ⏱️ Chronotope (Blommaert)
The concept that language use is inseparable from specific times and places. Different contexts (classroom vs. home, formal vs. informal) shape which languages and varieties are considered appropriate or valued.

#### 🎭 Identity Negotiation
The ongoing process of navigating multiple linguistic identities, especially the feeling of being "not enough" or "too much" in different cultural and linguistic contexts.

### Research Foundation

This project builds on research in sociolinguistics, multilingualism, and linguistic anthropology, particularly work by:
- **Sara Hillman** on linguistic shame and insecurity
- **Jan Blommaert** on sociolinguistic scales and chronotopes
- **Ofelia García** on translanguaging pedagogy
- Studies on Gulf multilingualism and expatriate identity

---

## 🚀 Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- No backend server required
- No dependencies or build tools needed

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd linguaspace
   ```

2. **Open in browser**
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     # Python 3
     python -m http.server 8000

     # Python 2
     python -m SimpleHTTPServer 8000

     # Node.js (with http-server)
     npx http-server
     ```

3. **Navigate to**
   - `http://localhost:8000` if using a local server
   - Or directly open the `index.html` file

### First Launch

On first visit, you'll see:
- A welcome message
- Featured "Story of the Week"
- 6 community categories
- Recent posts from all categories

---

## 📁 Project Structure

```
linguaspace/
├── index.html              # Main HTML structure
├── css/
│   ├── main.css           # Core styles, variables, typography
│   ├── components.css     # Cards, buttons, forms, modals
│   ├── layout.css         # Grid system, responsive design
│   └── animations.css     # Micro-interactions, transitions
├── js/
│   ├── data.js           # Sample posts and comments data
│   ├── voting.js         # Upvote/downvote system
│   ├── comments.js       # Comment rendering and threading
│   ├── posts.js          # Post display and modal
│   ├── filters.js        # Filtering and sorting logic
│   └── main.js           # App initialization, navigation
├── assets/
│   └── icons/            # (Optional) Custom icons
└── README.md             # This file
```

### File Descriptions

#### HTML
- **index.html**: Complete semantic HTML structure with accessibility features

#### CSS (BEM Methodology)
- **main.css**: CSS variables, base styles, typography, container
- **components.css**: Post cards, category cards, buttons, forms, modals, comments
- **layout.css**: Responsive grid system, breakpoints, utilities
- **animations.css**: Keyframe animations, transitions, micro-interactions

#### JavaScript (Modular ES6+)
- **data.js**: 40 sample posts across 6 categories, comments, trending topics
- **voting.js**: Voting system with localStorage, vote animations
- **comments.js**: Comment rendering, threading, time formatting
- **posts.js**: Post card rendering, modal, stats, featured post
- **filters.js**: Advanced filtering, sorting algorithms, search
- **main.js**: App initialization, navigation, form submission, modals

---

## 🛠️ Technologies Used

### Frontend
- **HTML5**: Semantic markup, accessibility features
- **CSS3**: Custom properties, Grid, Flexbox, animations
- **JavaScript (ES6+)**: Classes, arrow functions, template literals, modules

### Storage
- **localStorage**: Client-side data persistence

### Design
- **Color Palette**:
  - Primary: `#5865F2` (Deep blue/purple)
  - Accent: `#FF6B6B` (Warm coral)
  - Background: `#F6F7F9` (Light gray)
  - Text: `#2C3E50` (Dark gray)
- **Typography**: System fonts (Inter, Roboto, Segoe UI)
- **Icons**: Emoji-based (universal compatibility)

### Architecture
- **No frameworks**: Pure vanilla JavaScript
- **No build process**: Works directly in browser
- **No dependencies**: Completely self-contained

---

## 📖 Usage Guide

### Browsing Posts

1. **Home Page**: View all recent posts
2. **Categories**: Click a category card to filter by topic
3. **Sorting**: Use the sort dropdown (Hot, New, Top)
4. **Search**: Type keywords to find specific stories

### Filtering

Use the filter bar to refine posts by:
- **Category**: Select a specific community
- **Language**: Filter by language used
- **Experience Type**: Shame, Pride, Negotiation, Code-Switching

Active filters appear as removable tags below the filter bar.

### Voting

- **Upvote** ⬆: Click to show support
- **Downvote** ⬇: Click to disagree (use sparingly!)
- **Click again** to remove your vote
- Votes are saved in your browser

### Commenting

1. Click any post to open detailed view
2. Read existing comments
3. Use sort options: Best, New, Controversial
4. Comments support up to 3 levels of nesting

### Sharing Your Story

1. Click **"Share Your Story"** button
2. Select a community category
3. Write your title and story (translanguaging welcome!)
4. Select languages used
5. Get an anonymous username (or regenerate)
6. Submit and see confetti celebration! 🎉

Your story appears immediately at the top of the feed.

### Keyboard Shortcuts

- **Ctrl/Cmd + K**: Focus search bar
- **Ctrl/Cmd + N**: Open new post modal
- **Escape**: Close any modal

---

## 💾 Data Persistence

### What's Stored Locally

The application uses browser localStorage for:

1. **Votes**: Your upvotes and downvotes
2. **Saved Posts**: Posts you bookmark
3. **User Stories**: Stories you submit
4. **Visit Status**: First-visit detection

### Data Format

```javascript
// Votes
linguaspace_votes: {
  posts: { postId: 'up' | 'down' },
  comments: { commentId: 'up' | 'down' }
}

// Saved posts
linguaspace_saved: [postId, postId, ...]

// User submissions
linguaspace_user_posts: [post, post, ...]

// Visit status
linguaspace_visited: 'true'
```

### Clearing Data

To reset the application:
```javascript
localStorage.clear();
location.reload();
```

Or use browser DevTools → Application → Local Storage → Clear All.

---

## 🎨 Design Philosophy

### Reddit-Inspired UX
- Familiar navigation and interaction patterns
- Upvote/downvote system for community validation
- Threaded comments for nuanced discussion
- Category-based organization

### Academic Professionalism
- Clean, readable typography
- Calming color palette
- Thoughtful micro-interactions
- Accessible design

### Community Focus
- Anonymous but warm
- Validation over judgment
- Safe space indicators
- Celebrating diversity

### Micro-Interactions
- Vote buttons bounce on click
- Cards lift on hover
- Smooth transitions throughout
- Confetti celebration for new posts
- Toast notifications for feedback

---

## 🔮 Future Enhancements

### Technical
- [ ] Dark mode toggle
- [ ] Export/import data functionality
- [ ] Backend integration for real persistence
- [ ] User authentication (optional)
- [ ] Real-time updates with WebSockets
- [ ] Progressive Web App (PWA) support

### Features
- [ ] Rich text editor for posts
- [ ] Image upload support
- [ ] @ mentions and notifications
- [ ] Post editing and deletion
- [ ] Report/moderation system
- [ ] User profiles and history
- [ ] Weekly digest emails
- [ ] Badge/achievement system

### Community
- [ ] Academic concept tooltips (interactive)
- [ ] Resource library with papers
- [ ] Discussion prompts and themes
- [ ] Monthly "Featured Contributor"
- [ ] Integration with research data collection

### Accessibility
- [ ] Screen reader optimizations
- [ ] High contrast mode
- [ ] Font size controls
- [ ] Dyslexia-friendly font option
- [ ] Multi-language UI translation

---

## 📊 Sample Data

The application includes **40 pre-populated posts**:
- **7 posts** in r/AccentAnxiety
- **7 posts** in r/CodeSwitchingStruggles
- **6 posts** in r/TranslanguagingWins
- **7 posts** in r/NotEnoughTooMuch
- **6 posts** in r/LanguagePolicing
- **7 posts** in r/MultilingualPride

Each post includes:
- Realistic vote counts (5-267 upvotes)
- Multiple comments with threading
- Diverse student identities
- Various languages and combinations
- Some featuring translanguaging

---

## 🤝 Community Guidelines

### Our Values
- **Validation over Judgment**: We support each other's experiences
- **Anonymity & Safety**: Share without fear of identification
- **Linguistic Diversity**: All languages, accents, and varieties are welcome
- **Empathy First**: Assume good faith and respond with kindness

### Encouraged
- Sharing personal linguistic experiences
- Offering support and validation
- Mixing languages naturally (translanguaging)
- Celebrating multilingual identity

### Not Allowed
- Correcting or policing others' language use
- Dismissing or minimizing experiences
- Attempting to identify anonymous users
- Harassment or discrimination

---

## 🔒 Privacy & Ethics

### Demo Application Notice
This is a **demonstration application** for academic purposes:
- Data is stored **locally** in your browser only
- No information is sent to external servers
- No analytics or tracking implemented
- No personal information collected

### In a Production Environment
If deployed for real use, consider:
- User consent and data privacy policies
- Moderation and reporting systems
- Professional mental health resources
- Institutional Review Board (IRB) approval for research
- GDPR/data protection compliance

---

## 📄 Credits

### Developed For
Carnegie Mellon University Qatar (CMU-Q)
Multimodal Project on Linguistic Identity in the Arabian Gulf

### Academic Framework
- **Sara Hillman**: Linguistic Shame research
- **Jan Blommaert**: Chronotope and sociolinguistic scales
- **Ofelia García**: Translanguaging pedagogy

### Design Inspiration
- Reddit community structure
- Modern forum UX patterns
- Academic research platforms

---

## 📞 Support & Feedback

### For Academic Use
- This project is part of coursework at CMU-Q
- For questions about the research, contact your instructor
- For technical issues, check browser console for errors

### Technical Support
- Ensure JavaScript is enabled
- Clear browser cache if experiencing issues
- Try in a different browser
- Check browser localStorage limits (usually 5-10MB)

---

## 🎓 License

This project is created for **academic purposes** as part of a university multimodal project on linguistic identity at CMU-Q.

**For Educational Use Only**

---

## 🙏 Acknowledgments

Special thanks to:
- **Multilingual students** whose experiences inspired this project
- **CMU-Q community** for supporting linguistic diversity research
- **Linguistic researchers** whose work provides the theoretical foundation
- **Open source community** for design patterns and inspiration

---

## 🌟 Final Note

LinguaSpace celebrates the beautiful complexity of multilingual identity. Every accent tells a story. Every code-switch is a bridge between worlds. Every mixed sentence is an act of linguistic creativity.

**You're not confused. You're linguistically rich. 🗣️✨**

---

**Built with 💙 for multilingual voices everywhere**

Version 1.0 | Last Updated: November 2024
