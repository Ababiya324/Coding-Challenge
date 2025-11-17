/**
 * Language Identity Map - Story Data
 * Contains student stories about linguistic experiences at CMU-Q
 */

const stories = [
    {
        id: 1,
        location: "Academic Building",
        coordinates: { x: 250, y: 210 },
        studentProfile: "International Student from Ethiopia",
        languages: ["English", "Amharic"],
        experienceType: "Linguistic Shame",
        story: "During a group presentation, my groupmate corrected my pronunciation in front of everyone. I felt my accent was 'wrong' even though my content was strong. The shame made me rehearse every word obsessively for weeks after.",
        academicConcept: "Linguistic Shame (Hillman, 2019)",
        timestamp: "2024-10-15",
        background: "International"
    },
    {
        id: 2,
        location: "University Center",
        coordinates: { x: 650, y: 210 },
        studentProfile: "Qatari National Student",
        languages: ["Arabic", "English"],
        experienceType: "Code-Switching",
        story: "في UC I was talking to my friend بالعربي about a programming assignment. An American student said 'can you speak English? We're all here.' I felt like my language was treated as excluding, not natural.",
        academicConcept: "Translanguaging",
        timestamp: "2024-09-22",
        background: "Qatari"
    },
    {
        id: 3,
        location: "Library",
        coordinates: { x: 250, y: 410 },
        studentProfile: "International Student from Pakistan",
        languages: ["Urdu", "English", "Punjabi"],
        experienceType: "Linguistic Shame",
        story: "A professor asked me to repeat myself three times in office hours. I could see their frustration. I started avoiding asking questions in class, even when I was confused. My grade suffered because I stayed silent.",
        academicConcept: "Linguistic Shame (Hillman, 2019)",
        timestamp: "2024-10-01",
        background: "International"
    },
    {
        id: 4,
        location: "Dining Area",
        coordinates: { x: 480, y: 410 },
        studentProfile: "GCC National from Saudi Arabia",
        languages: ["Arabic", "English"],
        experienceType: "Linguistic Pride",
        story: "I was speaking Arabic with friends from different Arab countries, mixing dialects and laughing. A professor walked by and said 'I love hearing the linguistic diversity here.' For once, my Arabic felt valued in this English-dominant space.",
        academicConcept: "Linguistic Pride",
        timestamp: "2024-11-05",
        background: "GCC"
    },
    {
        id: 5,
        location: "Academic Building",
        coordinates: { x: 250, y: 210 },
        studentProfile: "International Student from India",
        languages: ["Hindi", "English", "Tamil"],
        experienceType: "Identity Negotiation",
        story: "In Computer Science class, I code-switched to Hindi when explaining an algorithm to another Indian student. The TA said 'English only please, for everyone's benefit.' But no one else was even listening to us.",
        academicConcept: "Chronotope (Blommaert)",
        timestamp: "2024-10-20",
        background: "International"
    },
    {
        id: 6,
        location: "Residence Halls",
        coordinates: { x: 690, y: 410 },
        studentProfile: "Qatari National Student",
        languages: ["Arabic", "English"],
        experienceType: "Linguistic Shame",
        story: "My Qatari friends criticized my Arabic, saying I sound 'too Western' or 'white-washed.' But in class, professors struggle with my accent. I'm not enough in either language, stuck in between.",
        academicConcept: "Linguistic Enoughness",
        timestamp: "2024-09-30",
        background: "Qatari"
    },
    {
        id: 7,
        location: "University Center",
        coordinates: { x: 650, y: 210 },
        studentProfile: "International Student from Morocco",
        languages: ["Arabic", "French", "English"],
        experienceType: "Code-Switching",
        story: "I naturally switch between Arabic, French, and English when I think. During a study session, someone said 'just pick one language!' But my brain doesn't work monolingually—this is how I process complex ideas.",
        academicConcept: "Translanguaging",
        timestamp: "2024-10-12",
        background: "International"
    },
    {
        id: 8,
        location: "Library",
        coordinates: { x: 250, y: 410 },
        studentProfile: "International Student from Philippines",
        languages: ["Tagalog", "English"],
        experienceType: "Linguistic Shame",
        story: "I was on a video call with my family in Tagalog in a study room. Someone knocked and gestured that I was being too loud. I felt like my language was noise, an intrusion. I started only speaking English on campus.",
        academicConcept: "Linguistic Shame (Hillman, 2019)",
        timestamp: "2024-10-08",
        background: "International"
    },
    {
        id: 9,
        location: "Common Outdoor Spaces",
        coordinates: { x: 850, y: 450 },
        studentProfile: "GCC National from UAE",
        languages: ["Arabic", "English"],
        experienceType: "Linguistic Pride",
        story: "During our Arabic heritage week, I performed a poem in Emirati dialect. Classmates who usually only hear me speak English came up amazed. I realized I'd been hiding a whole part of myself to fit in academically.",
        academicConcept: "Linguistic Pride",
        timestamp: "2024-11-10",
        background: "GCC"
    },
    {
        id: 10,
        location: "Academic Building",
        coordinates: { x: 250, y: 210 },
        studentProfile: "International Student from Lebanon",
        languages: ["Arabic", "French", "English"],
        experienceType: "Identity Negotiation",
        story: "I answered a question mixing Arabic and English—translanguaging naturally. The professor said 'that's interesting, but can you say it in proper English?' As if my multilingual expression wasn't 'proper' or legitimate.",
        academicConcept: "Translanguaging",
        timestamp: "2024-09-18",
        background: "International"
    },
    {
        id: 11,
        location: "Dining Area",
        coordinates: { x: 480, y: 410 },
        studentProfile: "International Student from Bangladesh",
        languages: ["Bengali", "English"],
        experienceType: "Linguistic Shame",
        story: "I ordered food and the server kept asking me to repeat myself. Students behind me in line were getting impatient. I felt like I was holding everyone up just by existing with my accent.",
        academicConcept: "Linguistic Shame (Hillman, 2019)",
        timestamp: "2024-10-25",
        background: "International"
    },
    {
        id: 12,
        location: "University Center",
        coordinates: { x: 650, y: 210 },
        studentProfile: "Qatari National Student",
        languages: ["Arabic", "English"],
        experienceType: "Linguistic Pride",
        story: "A new international student asked me to teach them Arabic greetings. Their genuine interest in learning made me feel proud of my language. I realized my bilingualism is a resource, not a deficit.",
        academicConcept: "Linguistic Pride",
        timestamp: "2024-11-12",
        background: "Qatari"
    },
    {
        id: 13,
        location: "Residence Halls",
        coordinates: { x: 690, y: 410 },
        studentProfile: "International Student from Egypt",
        languages: ["Arabic", "English"],
        experienceType: "Code-Switching",
        story: "Late night in the dorms, we have the best conversations switching between Arabic and English. Each language carries different emotional weight. When we code-switch, we're not confused—we're expressing ourselves fully.",
        academicConcept: "Translanguaging",
        timestamp: "2024-10-30",
        background: "International"
    },
    {
        id: 14,
        location: "Academic Building",
        coordinates: { x: 250, y: 210 },
        studentProfile: "GCC National from Bahrain",
        languages: ["Arabic", "English"],
        experienceType: "Identity Negotiation",
        story: "In a literature class discussing Arab poets, I offered to read the original Arabic. Professor said 'let's stick to the translation so everyone understands.' My access to the original text was dismissed as irrelevant.",
        academicConcept: "Chronotope (Blommaert)",
        timestamp: "2024-09-28",
        background: "GCC"
    },
    {
        id: 15,
        location: "Library",
        coordinates: { x: 250, y: 410 },
        studentProfile: "International Student from Syria",
        languages: ["Arabic", "English"],
        experienceType: "Linguistic Shame",
        story: "I was studying alone, thinking in Arabic and taking notes in English. Someone asked 'why do you mix languages in your notes? It's so confusing.' I felt judged for my natural cognitive process.",
        academicConcept: "Translanguaging",
        timestamp: "2024-10-18",
        background: "International"
    },
    {
        id: 16,
        location: "Common Outdoor Spaces",
        coordinates: { x: 850, y: 450 },
        studentProfile: "International Student from Nigeria",
        languages: ["English", "Yoruba", "Pidgin"],
        experienceType: "Identity Negotiation",
        story: "I speak English natively but with a Nigerian accent. People assume I'm an ESL student. I constantly have to prove my English proficiency despite it being my first language. The colonial hierarchy is alive and well.",
        academicConcept: "Linguistic Enoughness",
        timestamp: "2024-11-01",
        background: "International"
    },
    {
        id: 17,
        location: "Dining Area",
        coordinates: { x: 480, y: 410 },
        studentProfile: "Qatari National Student",
        languages: ["Arabic", "English"],
        experienceType: "Code-Switching",
        story: "كنت أتكلم with friends about a difficult exam بالعربي والانجليزي mixed. This is how we process stress. Our translanguaging isn't confusion—it's cultural fluency. It's how we navigate our bilingual reality.",
        academicConcept: "Translanguaging",
        timestamp: "2024-10-22",
        background: "Qatari"
    },
    {
        id: 18,
        location: "University Center",
        coordinates: { x: 650, y: 210 },
        studentProfile: "International Student from Jordan",
        languages: ["Arabic", "English"],
        experienceType: "Linguistic Pride",
        story: "During a presentation on Middle Eastern politics, I cited sources in Arabic and translated them myself. My professor praised my bilingual research skills. Finally, my Arabic was seen as academic capital, not a barrier.",
        academicConcept: "Linguistic Pride",
        timestamp: "2024-11-08",
        background: "International"
    },
    {
        id: 19,
        location: "Residence Halls",
        coordinates: { x: 690, y: 410 },
        studentProfile: "GCC National from Kuwait",
        languages: ["Arabic", "English"],
        experienceType: "Identity Negotiation",
        story: "My roommate asked why I 'put on' a different accent when speaking English vs Arabic. But these aren't performances—they're genuine parts of my identity. I contain multitudes, and that's not fake.",
        academicConcept: "Linguistic Identity",
        timestamp: "2024-09-25",
        background: "GCC"
    },
    {
        id: 20,
        location: "Academic Building",
        coordinates: { x: 250, y: 210 },
        studentProfile: "International Student from France",
        languages: ["French", "English", "Arabic"],
        experienceType: "Linguistic Shame",
        story: "I pronounced an English word with a French accent and the class laughed. The professor didn't correct them. I felt humiliated. Now I rehearse every presentation 20 times to neutralize my accent.",
        academicConcept: "Linguistic Shame (Hillman, 2019)",
        timestamp: "2024-10-05",
        background: "International"
    }
];

// Location coordinates for pin placement on the map
const locationCoordinates = {
    "Academic Building": { x: 250, y: 210 },
    "University Center": { x: 650, y: 210 },
    "Library": { x: 250, y: 410 },
    "Dining Area": { x: 480, y: 410 },
    "Residence Halls": { x: 690, y: 410 },
    "Common Outdoor Spaces": { x: 850, y: 450 }
};

// Experience type colors for visual coding
const experienceColors = {
    "Linguistic Shame": "#C41230",
    "Linguistic Pride": "#4CAF50",
    "Code-Switching": "#2196F3",
    "Identity Negotiation": "#FFC107"
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { stories, locationCoordinates, experienceColors };
}
