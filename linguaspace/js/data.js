// LinguaSpace - Sample Data
// 40 posts across 6 categories with comments

const categories = [
    {
        id: 'AccentAnxiety',
        name: 'r/AccentAnxiety',
        icon: '🎭',
        description: 'Stories about accent-related insecurity and judgment',
        color: '#E74C3C'
    },
    {
        id: 'CodeSwitchingStruggles',
        name: 'r/CodeSwitchingStruggles',
        icon: '🔄',
        description: 'The daily labor of switching between linguistic identities',
        color: '#9B59B6'
    },
    {
        id: 'TranslanguagingWins',
        name: 'r/TranslanguagingWins',
        icon: '🌐',
        description: 'Celebrating moments of mixing languages successfully',
        color: '#2ECC71'
    },
    {
        id: 'NotEnoughTooMuch',
        name: 'r/NotEnoughTooMuch',
        icon: '⚖️',
        description: 'Feeling \'not Arab enough\' or \'too foreign\'',
        color: '#F39C12'
    },
    {
        id: 'LanguagePolicing',
        name: 'r/LanguagePolicing',
        icon: '🚨',
        description: 'When others correct or police your language use',
        color: '#3498DB'
    },
    {
        id: 'MultilingualPride',
        name: 'r/MultilingualPride',
        icon: '✨',
        description: 'Celebrating our multilingual identities',
        color: '#1ABC9C'
    }
];

const posts = [
    // AccentAnxiety Posts (7 posts)
    {
        id: 1,
        category: 'AccentAnxiety',
        username: 'InternationalStudent_23',
        title: 'Professor asked me to repeat myself three times in class',
        content: 'I was answering a question and the professor kept saying "sorry, what?" My answer was correct but my accent made them not take me seriously. Now I don\'t volunteer answers anymore.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 47,
        downvotes: 2,
        commentCount: 12,
        timePosted: '2024-11-16T14:30:00',
        academicConcept: 'Linguistic Shame',
        translanguaging: false,
        featured: true
    },
    {
        id: 2,
        category: 'AccentAnxiety',
        username: 'QatariVoice_89',
        title: 'My Arabic accent in English makes people underestimate me',
        content: 'People assume I\'m less educated or less intelligent because of my accent. I have a 4.0 GPA in engineering but still get talked down to in group projects.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 62,
        downvotes: 1,
        commentCount: 15,
        timePosted: '2024-11-15T09:20:00',
        academicConcept: 'Chronotope',
        translanguaging: false
    },
    {
        id: 3,
        category: 'AccentAnxiety',
        username: 'MultilingualNomad',
        title: 'I rehearse what I\'m going to say before speaking in class',
        content: 'I literally practice sentences in my head multiple times before raising my hand. Sometimes I just stay silent because I\'m afraid my pronunciation will be judged.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 85,
        downvotes: 3,
        commentCount: 18,
        timePosted: '2024-11-14T16:45:00',
        academicConcept: 'Linguistic Shame',
        translanguaging: false
    },
    {
        id: 4,
        category: 'AccentAnxiety',
        username: 'SouthAsianScholar_12',
        title: 'Called customer service and they couldn\'t understand me',
        content: 'The person kept asking me to repeat myself and finally transferred me to someone else. Made me feel like my English isn\'t good enough even though I\'ve been speaking it my whole life.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 54,
        downvotes: 2,
        commentCount: 9,
        timePosted: '2024-11-13T11:30:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 5,
        category: 'AccentAnxiety',
        username: 'GulfStudent_2025',
        title: 'My "th" sounds apparently make me sound "cute"',
        content: 'A classmate said my accent is "cute" when I struggle with "th" sounds. I\'m not trying to be cute, I\'m trying to communicate professionally in a seminar.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 71,
        downvotes: 4,
        commentCount: 14,
        timePosted: '2024-11-12T14:00:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 6,
        category: 'AccentAnxiety',
        username: 'BilingualBrain_47',
        title: 'I avoid phone calls because of accent anxiety',
        content: 'I\'d rather email or text for everything because phone calls stress me out. People can\'t see my face or body language, so they judge me entirely on my voice.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 43,
        downvotes: 1,
        commentCount: 8,
        timePosted: '2024-11-11T10:15:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 7,
        category: 'AccentAnxiety',
        username: 'AfricanDiaspora_93',
        title: 'Told to "work on my accent" in job interview feedback',
        content: 'Got rejected from an internship and the feedback mentioned "communication skills" specifically about my accent. My technical skills were praised but apparently my accent is a problem.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 103,
        downvotes: 5,
        commentCount: 22,
        timePosted: '2024-11-10T13:50:00',
        academicConcept: 'Chronotope',
        translanguaging: false
    },

    // CodeSwitchingStruggles Posts (7 posts)
    {
        id: 8,
        category: 'CodeSwitchingStruggles',
        username: 'TrilingualStudent_21',
        title: 'Exhausted from switching between languages all day',
        content: 'Arabic with family at breakfast, English in classes, Hindi with friends at lunch, back to English for work, then Arabic at home. I feel like I\'m never just myself.',
        languages: ['Arabic', 'English', 'Hindi'],
        experienceType: 'Code-Switching',
        upvotes: 91,
        downvotes: 2,
        commentCount: 16,
        timePosted: '2024-11-16T17:20:00',
        academicConcept: 'Identity Negotiation',
        translanguaging: false
    },
    {
        id: 9,
        category: 'CodeSwitchingStruggles',
        username: 'CodeSwitcher_Daily',
        title: 'I accidentally code-switched mid-presentation',
        content: 'Was presenting my research and my brain just... switched to Arabic for a whole sentence. The confused looks from the panel made me want to disappear.',
        languages: ['Arabic', 'English'],
        experienceType: 'Code-Switching',
        upvotes: 67,
        downvotes: 3,
        commentCount: 11,
        timePosted: '2024-11-15T14:30:00',
        academicConcept: null,
        translanguaging: true
    },
    {
        id: 10,
        category: 'CodeSwitchingStruggles',
        username: 'ProfessionalFace_101',
        title: 'My "professional voice" doesn\'t sound like me',
        content: 'When I switch to my "professional English" voice for meetings, I feel like I\'m performing someone else. My real personality comes out in Arabic but that\'s not "professional" here.',
        languages: ['English', 'Arabic'],
        experienceType: 'Code-Switching',
        upvotes: 78,
        downvotes: 1,
        commentCount: 13,
        timePosted: '2024-11-14T11:00:00',
        academicConcept: 'Chronotope',
        translanguaging: false
    },
    {
        id: 11,
        category: 'CodeSwitchingStruggles',
        username: 'DualIdentity_88',
        title: 'Can\'t tell jokes in English the way I can in Arabic',
        content: 'My humor doesn\'t translate. I\'m funny in Arabic but my jokes fall flat in English. It\'s like losing part of my personality every time I switch.',
        languages: ['Arabic', 'English'],
        experienceType: 'Identity Negotiation',
        upvotes: 82,
        downvotes: 2,
        commentCount: 14,
        timePosted: '2024-11-13T16:45:00',
        academicConcept: 'Identity Negotiation',
        translanguaging: false
    },
    {
        id: 12,
        category: 'CodeSwitchingStruggles',
        username: 'EmiratiEngineer_45',
        title: 'Family says I "show off" when I speak English at home',
        content: 'I\'m not showing off, I\'m just thinking in English after a full day of classes! But my family thinks I\'m being pretentious when I accidentally use English words.',
        languages: ['Arabic', 'English'],
        experienceType: 'Code-Switching',
        upvotes: 56,
        downvotes: 4,
        commentCount: 10,
        timePosted: '2024-11-12T19:30:00',
        academicConcept: null,
        translanguaging: true
    },
    {
        id: 13,
        category: 'CodeSwitchingStruggles',
        username: 'LanguageJuggler_67',
        title: 'Forgot how to say something in BOTH languages',
        content: 'Brain freeze moment: couldn\'t remember the word in English or Arabic. Just stood there like a buffering computer. This is what constant code-switching does to you.',
        languages: ['Arabic', 'English'],
        experienceType: 'Code-Switching',
        upvotes: 94,
        downvotes: 3,
        commentCount: 17,
        timePosted: '2024-11-11T15:20:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 14,
        category: 'CodeSwitchingStruggles',
        username: 'BilingualBurnout_34',
        title: 'Sometimes I just want to speak ONE language all day',
        content: 'The mental load of switching is real. By evening I\'m exhausted from translating my thoughts all day. Anyone else feel this?',
        languages: ['Multilingual'],
        experienceType: 'Code-Switching',
        upvotes: 108,
        downvotes: 2,
        commentCount: 21,
        timePosted: '2024-11-10T20:00:00',
        academicConcept: null,
        translanguaging: false
    },

    // TranslanguagingWins Posts (6 posts)
    {
        id: 15,
        category: 'TranslanguagingWins',
        username: 'MixedLanguageMagic',
        title: 'Professor encouraged us to mix languages in our essays!',
        content: 'For our linguistic identity project, the professor said we can write in whatever mix of languages feels natural. Finally feels liberating to not separate my languages!',
        languages: ['Multilingual'],
        experienceType: 'Pride',
        upvotes: 127,
        downvotes: 4,
        commentCount: 19,
        timePosted: '2024-11-16T10:30:00',
        academicConcept: 'Translanguaging',
        translanguaging: false
    },
    {
        id: 16,
        category: 'TranslanguagingWins',
        username: 'ArabicEnglishFusion',
        title: 'My best ideas come when I stop trying to pick one language',
        content: 'Realized my most creative thinking happens when I let English and Arabic flow together naturally. يعني why choose when both languages can work together?',
        languages: ['Arabic', 'English'],
        experienceType: 'Pride',
        upvotes: 89,
        downvotes: 2,
        commentCount: 12,
        timePosted: '2024-11-15T13:15:00',
        academicConcept: 'Translanguaging',
        translanguaging: true
    },
    {
        id: 17,
        category: 'TranslanguagingWins',
        username: 'TrilingualThriver_88',
        title: 'Found friends who understand my language mixing!',
        content: 'Met a group that also mixes languages naturally. No judgment, no "speak properly" - just authentic multilingual communication. This is what community feels like.',
        languages: ['Multilingual'],
        experienceType: 'Pride',
        upvotes: 96,
        downvotes: 1,
        commentCount: 15,
        timePosted: '2024-11-14T09:40:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 18,
        category: 'TranslanguagingWins',
        username: 'LinguisticFreedom_42',
        title: 'Gave a presentation mixing three languages and nailed it',
        content: 'Presented my research using English technical terms, Arabic cultural concepts, and Urdu examples. The professor called it "brilliantly multilingual." I felt seen.',
        languages: ['English', 'Arabic', 'Urdu'],
        experienceType: 'Pride',
        upvotes: 112,
        downvotes: 3,
        commentCount: 17,
        timePosted: '2024-11-13T14:20:00',
        academicConcept: 'Translanguaging',
        translanguaging: true
    },
    {
        id: 19,
        category: 'TranslanguagingWins',
        username: 'MultilingualPoet_77',
        title: 'Wrote a poem in four languages and won a contest',
        content: 'My poem wove together Arabic, English, French, and Hindi. The judges said it captured the multilingual experience perfectly. Crying happy tears!',
        languages: ['Arabic', 'English', 'French', 'Hindi'],
        experienceType: 'Pride',
        upvotes: 156,
        downvotes: 2,
        commentCount: 24,
        timePosted: '2024-11-12T11:50:00',
        academicConcept: 'Translanguaging',
        translanguaging: true
    },
    {
        id: 20,
        category: 'TranslanguagingWins',
        username: 'CodeMixerPro',
        title: 'My bilingual notes helped the whole study group',
        content: 'Study group asked to use my notes that mix English and Arabic. Turns out my "messy" language mixing actually makes complex concepts clearer!',
        languages: ['Arabic', 'English'],
        experienceType: 'Pride',
        upvotes: 73,
        downvotes: 1,
        commentCount: 11,
        timePosted: '2024-11-11T16:30:00',
        academicConcept: null,
        translanguaging: true
    },

    // NotEnoughTooMuch Posts (7 posts)
    {
        id: 21,
        category: 'NotEnoughTooMuch',
        username: 'InBetweenIdentity_56',
        title: 'Too Western for Qatar, too Arab for America',
        content: 'When I\'m in Qatar, people say I\'m too Americanized. When I visit the US, people see me as too foreign. I don\'t fully belong anywhere.',
        languages: ['English'],
        experienceType: 'Identity Negotiation',
        upvotes: 134,
        downvotes: 3,
        commentCount: 26,
        timePosted: '2024-11-16T12:00:00',
        academicConcept: 'Identity Negotiation',
        translanguaging: false
    },
    {
        id: 22,
        category: 'NotEnoughTooMuch',
        username: 'ThirdCultureKid_91',
        title: 'My Arabic isn\'t "pure" enough for some people',
        content: 'I mix dialects and use English words because that\'s how I learned. But some people act like my Arabic is broken or inferior. مش كفاية apparently.',
        languages: ['Arabic', 'English'],
        experienceType: 'Linguistic Shame',
        upvotes: 88,
        downvotes: 4,
        commentCount: 16,
        timePosted: '2024-11-15T15:45:00',
        academicConcept: 'Linguistic Shame',
        translanguaging: true
    },
    {
        id: 23,
        category: 'NotEnoughTooMuch',
        username: 'DiasporaVoice_33',
        title: 'Cousins laugh at my accent when I speak Arabic',
        content: 'Grew up abroad and my Arabic has an accent. My cousins think it\'s funny to mimic me. Makes me not want to try speaking Arabic anymore.',
        languages: ['Arabic'],
        experienceType: 'Linguistic Shame',
        upvotes: 79,
        downvotes: 2,
        commentCount: 13,
        timePosted: '2024-11-14T18:30:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 24,
        category: 'NotEnoughTooMuch',
        username: 'HalfHalfWhole_99',
        title: 'Constantly explaining my background to people',
        content: 'Where are you from? No, where are you REALLY from? Where are your parents from? I\'m tired of the interrogation about my identity and belonging.',
        languages: ['English'],
        experienceType: 'Identity Negotiation',
        upvotes: 142,
        downvotes: 5,
        commentCount: 28,
        timePosted: '2024-11-13T10:20:00',
        academicConcept: 'Identity Negotiation',
        translanguaging: false
    },
    {
        id: 25,
        category: 'NotEnoughTooMuch',
        username: 'InternationalSoul_24',
        title: 'Don\'t feel Arab enough to join Arab student groups',
        content: 'I want to join but I\'m scared they\'ll judge my Arabic or say I\'m not "really" Arab. Imposter syndrome is real.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 67,
        downvotes: 3,
        commentCount: 14,
        timePosted: '2024-11-12T14:40:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 26,
        category: 'NotEnoughTooMuch',
        username: 'NeitherNorBoth_88',
        title: 'Code-switching makes me feel like a fraud everywhere',
        content: 'When I switch between languages, I feel like I\'m faking it in both. Like I\'m not authentic in any language or culture.',
        languages: ['Multilingual'],
        experienceType: 'Identity Negotiation',
        upvotes: 95,
        downvotes: 2,
        commentCount: 18,
        timePosted: '2024-11-11T11:00:00',
        academicConcept: 'Identity Negotiation',
        translanguaging: false
    },
    {
        id: 27,
        category: 'NotEnoughTooMuch',
        username: 'BetweenWorlds_17',
        title: 'My "home" language feels foreign now',
        content: 'Spent so much time speaking English that my mother tongue feels uncomfortable. But English isn\'t really mine either. Lost in translation.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 86,
        downvotes: 4,
        commentCount: 15,
        timePosted: '2024-11-10T16:50:00',
        academicConcept: null,
        translanguaging: false
    },

    // LanguagePolicing Posts (6 posts)
    {
        id: 28,
        category: 'LanguagePolicing',
        username: 'CorrectedConstantly_44',
        title: 'Classmate keeps correcting my English grammar publicly',
        content: 'In the middle of me making a point, they interrupt to correct my grammar. It\'s not helpful, it\'s humiliating. My ideas matter more than perfect grammar.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 118,
        downvotes: 6,
        commentCount: 21,
        timePosted: '2024-11-16T11:15:00',
        academicConcept: 'Linguistic Shame',
        translanguaging: false
    },
    {
        id: 29,
        category: 'LanguagePolicing',
        username: 'PoliceTarget_92',
        title: 'TA said my English writing is "too simple"',
        content: 'Got my essay back with comments that my writing is "simplistic" because I don\'t use complex vocab. I\'m communicating clearly - isn\'t that the point?',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 71,
        downvotes: 3,
        commentCount: 13,
        timePosted: '2024-11-15T16:20:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 30,
        category: 'LanguagePolicing',
        username: 'ArabicGuardian_28',
        title: 'Uncle says I\'m "ruining" Arabic by mixing English',
        content: 'He acts like language is something pure that I\'m contaminating. بس this is how my generation speaks! Language evolves.',
        languages: ['Arabic', 'English'],
        experienceType: 'Negotiation',
        upvotes: 83,
        downvotes: 7,
        commentCount: 16,
        timePosted: '2024-11-14T13:30:00',
        academicConcept: null,
        translanguaging: true
    },
    {
        id: 31,
        category: 'LanguagePolicing',
        username: 'SpeakProperly_Tired',
        title: '"Speak properly" - what does that even mean?',
        content: 'I AM speaking properly. This is how I speak. Just because it doesn\'t match your standard doesn\'t make it wrong.',
        languages: ['English'],
        experienceType: 'Negotiation',
        upvotes: 101,
        downvotes: 4,
        commentCount: 19,
        timePosted: '2024-11-13T09:45:00',
        academicConcept: 'Chronotope',
        translanguaging: false
    },
    {
        id: 32,
        category: 'LanguagePolicing',
        username: 'MultilingualReality_66',
        title: 'Manager said I should "avoid accent" in client meetings',
        content: 'How am I supposed to avoid my accent? It\'s part of who I am. This feels discriminatory honestly.',
        languages: ['English'],
        experienceType: 'Linguistic Shame',
        upvotes: 147,
        downvotes: 5,
        commentCount: 27,
        timePosted: '2024-11-12T10:30:00',
        academicConcept: 'Chronotope',
        translanguaging: false
    },
    {
        id: 33,
        category: 'LanguagePolicing',
        username: 'DefendingMyVoice_11',
        title: 'Someone asked "why don\'t you take accent reduction classes?"',
        content: 'Why don\'t YOU take a class in respecting linguistic diversity? My accent is not a problem to be fixed.',
        languages: ['English'],
        experienceType: 'Negotiation',
        upvotes: 178,
        downvotes: 8,
        commentCount: 31,
        timePosted: '2024-11-11T14:00:00',
        academicConcept: null,
        translanguaging: false
    },

    // MultilingualPride Posts (7 posts)
    {
        id: 34,
        category: 'MultilingualPride',
        username: 'ProudMultilingual_55',
        title: 'I can dream in three languages and that\'s beautiful',
        content: 'Sometimes my dreams are in Arabic, sometimes English, sometimes a mix. My brain is a multilingual wonderland and I love it.',
        languages: ['Arabic', 'English', 'Other'],
        experienceType: 'Pride',
        upvotes: 201,
        downvotes: 3,
        commentCount: 33,
        timePosted: '2024-11-16T08:45:00',
        academicConcept: null,
        translanguaging: true
    },
    {
        id: 35,
        category: 'MultilingualPride',
        username: 'LanguageGift_78',
        title: 'My multilingualism helped me land an internship!',
        content: 'Company specifically wanted someone who could navigate Arabic and English contexts. My "liability" became my greatest asset!',
        languages: ['Arabic', 'English'],
        experienceType: 'Pride',
        upvotes: 167,
        downvotes: 2,
        commentCount: 25,
        timePosted: '2024-11-15T12:30:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 36,
        category: 'MultilingualPride',
        username: 'CognitiveAdvantage_22',
        title: 'Being multilingual made me better at problem-solving',
        content: 'Research shows multilingual brains are more flexible. I see it in how I approach complex problems from multiple angles. Our linguistic diversity is cognitive strength!',
        languages: ['English'],
        experienceType: 'Pride',
        upvotes: 143,
        downvotes: 4,
        commentCount: 22,
        timePosted: '2024-11-14T10:15:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 37,
        category: 'MultilingualPride',
        username: 'GlobalCitizen_99',
        title: 'I can connect with people across cultures',
        content: 'My multilingualism isn\'t just about languages - it\'s about understanding different worldviews. I can bridge communities that others can\'t reach.',
        languages: ['Multilingual'],
        experienceType: 'Pride',
        upvotes: 189,
        downvotes: 5,
        commentCount: 29,
        timePosted: '2024-11-13T15:50:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 38,
        category: 'MultilingualPride',
        username: 'RichNotPoor_84',
        title: 'I\'m linguistically RICH, not confused',
        content: 'Stop calling multilingualism "confusion". I have access to multiple ways of thinking, expressing, and being. That\'s richness, not deficit.',
        languages: ['English'],
        experienceType: 'Pride',
        upvotes: 224,
        downvotes: 6,
        commentCount: 38,
        timePosted: '2024-11-12T09:20:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 39,
        category: 'MultilingualPride',
        username: 'FutureIsMultilingual',
        title: 'Teaching my kids to be proud of their multilingualism',
        content: 'Breaking the cycle of linguistic shame. My children will grow up celebrating all their languages, not hiding them.',
        languages: ['Multilingual'],
        experienceType: 'Pride',
        upvotes: 156,
        downvotes: 3,
        commentCount: 24,
        timePosted: '2024-11-11T13:40:00',
        academicConcept: null,
        translanguaging: false
    },
    {
        id: 40,
        category: 'MultilingualPride',
        username: 'UniqueVoice_51',
        title: 'My accent is my story, and I\'m keeping it',
        content: 'Every pronunciation, every code-switch, every mixed sentence tells the story of where I\'ve been and who I am. I\'m done apologizing for my voice.',
        languages: ['English'],
        experienceType: 'Pride',
        upvotes: 267,
        downvotes: 7,
        commentCount: 42,
        timePosted: '2024-11-10T11:00:00',
        academicConcept: 'Identity Negotiation',
        translanguaging: false
    }
];

// Comments data
const comments = [
    // Comments for Post 1
    { id: 1, postId: 1, parentId: null, username: 'MultilingualVoice_89', content: 'I felt this so deeply. You\'re not alone. This happened to me in my engineering class last semester.', upvotes: 15, downvotes: 0, timePosted: '2024-11-16T15:45:00' },
    { id: 2, postId: 1, parentId: 1, username: 'SupportiveStudent_22', content: 'Same here. It\'s their problem, not yours. Your accent doesn\'t diminish your intelligence.', upvotes: 8, downvotes: 0, timePosted: '2024-11-16T16:20:00' },
    { id: 3, postId: 1, parentId: null, username: 'EmpathyFirst_44', content: 'That professor needs training in linguistic diversity. This is unacceptable.', upvotes: 23, downvotes: 1, timePosted: '2024-11-16T17:00:00' },

    // Comments for Post 2
    { id: 4, postId: 2, parentId: null, username: 'Solidarity_77', content: 'People really equate accent with intelligence and it\'s so frustrating. You deserve better.', upvotes: 12, downvotes: 0, timePosted: '2024-11-15T10:30:00' },
    { id: 5, postId: 2, parentId: null, username: 'EngineeringAlly_93', content: 'Fellow engineering student here. Your 4.0 speaks louder than any accent. Keep crushing it! 💪', upvotes: 19, downvotes: 0, timePosted: '2024-11-15T11:15:00' },

    // Comments for Post 3
    { id: 6, postId: 3, parentId: null, username: 'SameBoat_101', content: 'I do this too! Thought I was the only one. It\'s exhausting.', upvotes: 31, downvotes: 0, timePosted: '2024-11-14T17:30:00' },
    { id: 7, postId: 3, parentId: 6, username: 'MultilingualNomad', content: 'So relieving to know others experience this. We need to talk about this more.', upvotes: 14, downvotes: 0, timePosted: '2024-11-14T18:00:00' },
    { id: 8, postId: 3, parentId: null, username: 'ValidationStation_56', content: 'Your ideas are valuable regardless of how they sound. I hope you find the courage to share them!', upvotes: 22, downvotes: 0, timePosted: '2024-11-14T19:00:00' },

    // Comments for Post 8
    { id: 9, postId: 8, parentId: null, username: 'MentalLoadReal_33', content: 'The mental exhaustion of this is REAL. Code-switching fatigue is a real phenomenon.', upvotes: 28, downvotes: 0, timePosted: '2024-11-16T18:00:00' },
    { id: 10, postId: 8, parentId: null, username: 'LinguisticLabor_88', content: 'Yes! It\'s invisible labor that people don\'t recognize. Wishing you rest.', upvotes: 17, downvotes: 0, timePosted: '2024-11-16T19:00:00' },

    // Comments for Post 15
    { id: 11, postId: 15, parentId: null, username: 'AcademicWin_42', content: 'This is what translanguaging pedagogy should look like! Your professor gets it.', upvotes: 34, downvotes: 0, timePosted: '2024-11-16T11:30:00' },
    { id: 12, postId: 15, parentId: 11, username: 'MixedLanguageMagic', content: 'Exactly! It feels revolutionary to have academic validation for how we actually communicate.', upvotes: 21, downvotes: 0, timePosted: '2024-11-16T12:00:00' },
    { id: 13, postId: 15, parentId: null, username: 'BlommaertFan_91', content: 'This recognizes the reality of chronotopes - different contexts allow different linguistic practices. Love this!', upvotes: 15, downvotes: 1, timePosted: '2024-11-16T13:00:00' },

    // Comments for Post 21
    { id: 14, postId: 21, parentId: null, username: 'ThirdCultureLife_67', content: 'The "too much/not enough" struggle is so real. You\'re enough exactly as you are.', upvotes: 41, downvotes: 0, timePosted: '2024-11-16T13:00:00' },
    { id: 15, postId: 21, parentId: null, username: 'InBetweenToo_23', content: 'I feel this in my soul. Sometimes being "in between" IS an identity of its own.', upvotes: 38, downvotes: 1, timePosted: '2024-11-16T14:00:00' },

    // Comments for Post 28
    { id: 16, postId: 28, parentId: null, username: 'StopCorrecting_99', content: 'That classmate needs to learn that communication > perfection. So rude.', upvotes: 32, downvotes: 0, timePosted: '2024-11-16T12:00:00' },
    { id: 17, postId: 28, parentId: null, username: 'IdeasMatter_44', content: 'Your ideas absolutely matter more. Keep contributing!', upvotes: 27, downvotes: 0, timePosted: '2024-11-16T13:30:00' },

    // Comments for Post 34
    { id: 18, postId: 34, parentId: null, username: 'DreamLanguages_88', content: 'I love this perspective! My dreams are multilingual too and it\'s magical.', upvotes: 46, downvotes: 0, timePosted: '2024-11-16T09:30:00' },
    { id: 19, postId: 34, parentId: 18, username: 'ProudMultilingual_55', content: 'Right?! It\'s like our brains are composing poetry across languages while we sleep.', upvotes: 33, downvotes: 0, timePosted: '2024-11-16T10:00:00' },

    // Comments for Post 40
    { id: 20, postId: 40, parentId: null, username: 'AccentPride_77', content: 'YES! Our accents are our stories. Never apologize for your voice! 🗣️', upvotes: 67, downvotes: 0, timePosted: '2024-11-10T12:00:00' },
    { id: 21, postId: 40, parentId: null, username: 'OwnYourVoice_31', content: 'This made me emotional. Thank you for this reminder. Our voices are valid.', upvotes: 54, downvotes: 1, timePosted: '2024-11-10T13:00:00' },
    { id: 22, postId: 40, parentId: 20, username: 'LinguisticIdentity_12', content: 'Every word of this. Our accents carry our histories and that\'s beautiful.', upvotes: 41, downvotes: 0, timePosted: '2024-11-10T14:00:00' },

    // Additional comments for highly engaged posts
    { id: 23, postId: 14, parentId: null, username: 'MentalHealth_Focus', content: 'This is a real form of burnout that needs recognition. Take care of yourself.', upvotes: 38, downvotes: 0, timePosted: '2024-11-10T21:00:00' },
    { id: 24, postId: 24, parentId: null, username: 'TiredOfQuestions_56', content: 'The "where are you REALLY from" question is so invalidating. I feel you.', upvotes: 52, downvotes: 1, timePosted: '2024-11-13T11:30:00' },
    { id: 25, postId: 33, parentId: null, username: 'AccentsAreValid_89', content: 'PREACH! Accent reduction classes? More like respect expansion classes for everyone else.', upvotes: 71, downvotes: 2, timePosted: '2024-11-11T15:00:00' },
    { id: 26, postId: 38, parentId: null, username: 'ReframeTheNarrative', content: 'Linguistic richness not confusion - I\'m using this from now on. Thank you!', upvotes: 63, downvotes: 0, timePosted: '2024-11-12T10:00:00' }
];

// Trending topics
const trendingTopics = [
    { tag: '#AccentJourney', count: 47 },
    { tag: '#LinguisticPride', count: 38 },
    { tag: '#Translanguaging', count: 34 },
    { tag: '#NotEnough', count: 29 },
    { tag: '#CodeSwitching', count: 26 },
    { tag: '#MultilingualMagic', count: 22 }
];

// Make data globally available
window.linguaSpaceData = {
    categories,
    posts,
    comments,
    trendingTopics
};
