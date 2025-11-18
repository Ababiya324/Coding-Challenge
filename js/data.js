// Student stories data for Language Identity Map
// Each story represents real linguistic experiences at CMU-Q

const storiesData = [
  {
    id: 1,
    location: "Academic Building",
    coordinates: { x: 35, y: 40 },
    studentProfile: "International Student from Ethiopia",
    languages: ["English", "Amharic"],
    experienceType: "Linguistic Shame",
    story: "During a group presentation, my groupmate corrected my pronunciation in front of everyone. I felt my accent was 'wrong' even though my content was strong.",
    academicConcept: "Linguistic Shame (Hillman, 2019)",
    timestamp: "2024-11-15"
  },
  {
    id: 2,
    location: "University Center",
    coordinates: { x: 55, y: 50 },
    studentProfile: "Qatari National",
    languages: ["Arabic", "English"],
    experienceType: "Code-Switching",
    story: "I automatically switch to English when discussing technical topics, even with Arabic-speaking friends. It feels natural but also like I'm losing part of myself.",
    academicConcept: "Translanguaging Practices",
    timestamp: "2024-11-10"
  },
  {
    id: 3,
    location: "Library",
    coordinates: { x: 65, y: 35 },
    studentProfile: "International Student from India",
    languages: ["English", "Hindi", "Tamil"],
    experienceType: "Linguistic Shame",
    story: "A professor asked me to 'speak more clearly' during office hours. I've been practicing American pronunciation ever since, hiding my natural accent.",
    academicConcept: "Linguistic Shame (Hillman, 2019)",
    timestamp: "2024-11-08"
  },
  {
    id: 4,
    location: "Dining Area",
    coordinates: { x: 45, y: 65 },
    studentProfile: "Lebanese Student",
    languages: ["Arabic", "French", "English"],
    experienceType: "Linguistic Pride",
    story: "My friends love when I mix Arabic, French, and English in one sentence. They say it sounds sophisticated and reflects who I really am.",
    academicConcept: "Translanguaging as Identity Expression",
    timestamp: "2024-11-12"
  },
  {
    id: 5,
    location: "Academic Building",
    coordinates: { x: 35, y: 45 },
    studentProfile: "International Student from Pakistan",
    languages: ["Urdu", "English"],
    experienceType: "Linguistic Shame",
    story: "I avoid speaking Urdu on campus because someone once said it 'sounds aggressive.' Now I code-switch even when calling my parents.",
    academicConcept: "Linguistic Policing and Shame",
    timestamp: "2024-10-28"
  },
  {
    id: 6,
    location: "Residence Halls",
    coordinates: { x: 75, y: 60 },
    studentProfile: "Saudi Student",
    languages: ["Arabic", "English"],
    experienceType: "Identity Negotiation",
    story: "My Saudi dialect is 'too informal' for some Qataris, and my English is 'not American enough' for international students. I'm constantly adjusting.",
    academicConcept: "Chronotope and Identity Navigation",
    timestamp: "2024-11-05"
  },
  {
    id: 7,
    location: "University Center",
    coordinates: { x: 50, y: 55 },
    studentProfile: "Filipino Student",
    languages: ["Tagalog", "English"],
    experienceType: "Linguistic Shame",
    story: "When I speak Tagalog with other Filipinos, I notice others staring. I started texting instead of speaking to avoid the uncomfortable attention.",
    academicConcept: "Linguistic Surveillance",
    timestamp: "2024-11-01"
  },
  {
    id: 8,
    location: "Library",
    coordinates: { x: 68, y: 38 },
    studentProfile: "Emirati Student",
    languages: ["Arabic", "English"],
    experienceType: "Linguistic Pride",
    story: "I insisted on using Arabic terms in my presentation about Gulf culture. The professor appreciated the authenticity, and it felt empowering.",
    academicConcept: "Linguistic Resistance",
    timestamp: "2024-11-14"
  },
  {
    id: 9,
    location: "Academic Building",
    coordinates: { x: 32, y: 42 },
    studentProfile: "Moroccan Student",
    languages: ["Darija", "French", "English", "Arabic"],
    experienceType: "Code-Switching",
    story: "كل day I switch between four languages. Sometimes I don't even notice which language I'm using until someone points it out.",
    academicConcept: "Translanguaging as Daily Practice",
    timestamp: "2024-11-09"
  },
  {
    id: 10,
    location: "Outdoor Spaces",
    coordinates: { x: 55, y: 25 },
    studentProfile: "Syrian Refugee Student",
    languages: ["Arabic", "English"],
    experienceType: "Linguistic Shame",
    story: "People assume I'm less intelligent when I speak with my accent. I've learned to stay quiet in large groups to avoid judgment.",
    academicConcept: "Linguistic Shame and Silence",
    timestamp: "2024-10-25"
  },
  {
    id: 11,
    location: "Dining Area",
    coordinates: { x: 48, y: 68 },
    studentProfile: "Qatari Student",
    languages: ["Arabic", "English"],
    experienceType: "Identity Negotiation",
    story: "I speak English with local friends to seem 'international' but Arabic with family to prove I'm still 'authentic.' It's exhausting.",
    academicConcept: "Identity Performance and Enoughness",
    timestamp: "2024-11-11"
  },
  {
    id: 12,
    location: "University Center",
    coordinates: { x: 52, y: 52 },
    studentProfile: "Egyptian Student",
    languages: ["Arabic", "English"],
    experienceType: "Linguistic Pride",
    story: "My Egyptian dialect makes people smile. I use humor and language to connect with others, and it's become my social superpower.",
    academicConcept: "Linguistic Capital",
    timestamp: "2024-11-13"
  },
  {
    id: 13,
    location: "Library",
    coordinates: { x: 62, y: 40 },
    studentProfile: "International Student from Turkey",
    languages: ["Turkish", "English", "Arabic"],
    experienceType: "Linguistic Shame",
    story: "I struggle to find the right words in English during discussions. The long pauses make me seem unprepared, even when I know the content.",
    academicConcept: "Linguistic Shame in Academic Spaces",
    timestamp: "2024-10-30"
  },
  {
    id: 14,
    location: "Residence Halls",
    coordinates: { x: 72, y: 58 },
    studentProfile: "Jordanian Student",
    languages: ["Arabic", "English"],
    experienceType: "Code-Switching",
    story: "My roommate and I switch between Arabic and English mid-sentence. It's our own private language that no one else understands.",
    academicConcept: "Translanguaging as Intimacy",
    timestamp: "2024-11-07"
  },
  {
    id: 15,
    location: "Academic Building",
    coordinates: { x: 38, y: 38 },
    studentProfile: "International Student from Bangladesh",
    languages: ["Bengali", "English"],
    experienceType: "Linguistic Shame",
    story: "A classmate mimicked my accent during a break. Everyone laughed. I haven't volunteered to speak in class since.",
    academicConcept: "Linguistic Bullying and Trauma",
    timestamp: "2024-10-22"
  },
  {
    id: 16,
    location: "Outdoor Spaces",
    coordinates: { x: 58, y: 28 },
    studentProfile: "Bahraini Student",
    languages: ["Arabic", "English"],
    experienceType: "Identity Negotiation",
    story: "I'm 'not Arab enough' for some students and 'not Western enough' for others. I navigate between worlds, never fully belonging to either.",
    academicConcept: "Third Space Identity",
    timestamp: "2024-11-06"
  },
  {
    id: 17,
    location: "University Center",
    coordinates: { x: 48, y: 48 },
    studentProfile: "Kuwaiti Student",
    languages: ["Arabic", "English"],
    experienceType: "Linguistic Pride",
    story: "I deliberately use Khaleeji Arabic slang in conversations. It's my way of asserting my Gulf identity in a diverse campus.",
    academicConcept: "Linguistic Assertion",
    timestamp: "2024-11-16"
  },
  {
    id: 18,
    location: "Dining Area",
    coordinates: { x: 42, y: 62 },
    studentProfile: "International Student from Nigeria",
    languages: ["Yoruba", "English"],
    experienceType: "Linguistic Shame",
    story: "Someone asked if I 'spoke African.' The ignorance hurt, but I just smiled and explained. I'm tired of educating others about my languages.",
    academicConcept: "Linguistic Microaggressions",
    timestamp: "2024-11-04"
  },
  {
    id: 19,
    location: "Library",
    coordinates: { x: 70, y: 42 },
    studentProfile: "Palestinian Student",
    languages: ["Arabic", "English"],
    experienceType: "Identity Negotiation",
    story: "Speaking Palestinian Arabic is political. Some embrace it, others critique it. Language is never just language for me—it's history.",
    academicConcept: "Language as Political Identity",
    timestamp: "2024-11-03"
  },
  {
    id: 20,
    location: "Outdoor Spaces",
    coordinates: { x: 52, y: 22 },
    studentProfile: "International Student from France",
    languages: ["French", "English", "Arabic"],
    experienceType: "Linguistic Pride",
    story: "Being trilingual at CMU-Q is an asset. I can connect with multiple groups and bridge cultural conversations. My languages are my strength.",
    academicConcept: "Multilingual Advantage",
    timestamp: "2024-11-17"
  }
];

// Campus locations for the map
const campusLocations = [
  { id: "academic", name: "Academic Building", x: 35, y: 40 },
  { id: "uc", name: "University Center", x: 52, y: 50 },
  { id: "library", name: "Library", x: 65, y: 38 },
  { id: "dining", name: "Dining Area", x: 45, y: 65 },
  { id: "residence", name: "Residence Halls", x: 73, y: 59 },
  { id: "outdoor", name: "Outdoor Spaces", x: 55, y: 25 }
];

// Academic concepts with definitions
const academicConcepts = {
  "Linguistic Shame": "The feeling of embarrassment or inadequacy about one's language use, accent, or multilingual identity (Hillman, 2019)",
  "Translanguaging": "The fluid use of multiple languages as a unified linguistic repertoire, rather than separate language systems (García & Wei, 2014)",
  "Chronotope": "The intersection of time and space where specific language practices and identities emerge (Blommaert, 2015)",
  "Enoughness": "The constant negotiation of being 'enough' in multiple cultural and linguistic contexts",
  "Linguistic Policing": "Social surveillance and correction of language use, often marginalizing non-dominant varieties",
  "Code-Switching": "Alternating between languages or language varieties within a conversation or social context"
};

// Export data for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { storiesData, campusLocations, academicConcepts };
}
