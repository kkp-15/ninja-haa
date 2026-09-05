/* Prompts for the English edition — all original.

   This is not a translation of the Japanese set. The whole game rests on how a
   word *sounds*, so the lines had to be rebuilt from English interjections that
   native speakers actually stretch and bend ("Huh?", "Sure.", "No way!").

   Shape: { word: the line everyone says, acts: [8 ways to say it] }
   With fewer than 8 players we take acts from the top, so the earlier ones are
   the easier reads and the later ones are the tricky ones. */
const THEMES = {
  basics: {
    label: 'Basics',
    desc: 'Start here. One syllable, eight completely different meanings.',
    list: [
      { word: 'Huh?', acts: ['Confused','You did not hear it','Annoyed','Suspicious','Amazed','Bored','Playfully teasing','Genuinely shocked'] },
      { word: 'Oh.', acts: ['Disappointed','It just clicked','Impressed','Pretending to care','Quietly hurt','Relieved','Suspicious','Delighted'] },
      { word: 'Wow.', acts: ['Truly amazed','Sarcastic','Horrified','Proud of someone','Faking enthusiasm','Overwhelmed','Jealous','Deeply moved'] },
      { word: 'Hey.', acts: ['Greeting a friend','Warning someone off','Trying to get attention','Angry','Surprised to see them','Flirting','Calming someone down','Suspicious'] },
      { word: 'Okay.', acts: ['Agreeing','Reluctant','Annoyed','Not really listening','Worried','Making up your mind','Confused','Sarcastic'] },
      { word: 'Yeah.', acts: ['Enthusiastic','Unsure','Bored','Sarcastic','Relieved','Reluctant','Excited','Half asleep'] },
      { word: 'Really?', acts: ['Genuinely surprised','Doubtful','Delighted','Disappointed','Sarcastic','Worried','Bored','Hearing gossip'] },
      { word: 'Hmm.', acts: ['Thinking it over','Suspicious','Impressed','Politely disagreeing','Bored','Tasting something good','Pretending to listen','Worried'] },
      { word: 'Sure.', acts: ['Happy to help','Reluctant','Sarcastic','Doubtful','Distracted','Firm and final','Shy','Annoyed'] },
      { word: 'Fine.', acts: ['Actually fine','Clearly not fine','Giving in','Annoyed','Relieved','Ice cold','Cheerful','Completely drained'] },
    ]
  },
  greetings: {
    label: 'Greetings',
    desc: 'The same hello changes with who is standing there.',
    list: [
      { word: 'Good morning.', acts: ['Cheerful','Barely awake','Awkward','To your boss','To a whole room','Annoyed','To someone you missed','Worried about them'] },
      { word: 'Thank you.', acts: ['Deeply grateful','Polite and formal','Sarcastic','Shy','In a rush','Close to tears','Reluctant','To a small child'] },
      { word: 'Sorry.', acts: ['Sincere','Not sorry at all','Embarrassed','Apologising for someone else','Squeezing past','Heartbroken','A light bump','In real trouble'] },
      { word: 'Excuse me.', acts: ['Politely','Trying to get past','Angry','Getting attention','You did not hear','Interrupting','Shocked at rudeness','Shy'] },
      { word: 'Goodbye.', acts: ['Casual','Final','Sad','Relieved','In a rush','To a child','Cold','Holding back tears'] },
      { word: 'Nice to meet you.', acts: ['Genuine','Nervous','At a formal event','Not interested','Meeting your hero','Awkward','Warm','Rushed'] },
    ]
  },
  work: {
    label: 'At work',
    desc: 'Safe for the office. Nobody gets embarrassed.',
    list: [
      { word: 'No problem.', acts: ['Genuinely happy to','Hiding irritation','Exhausted','Reassuring them','Dismissive','Confident','Not sure at all','In a rush'] },
      { word: 'Got it.', acts: ['Confident','Lost but pretending','Annoyed','Excited','Tired','Polite','Relieved','Suspicious'] },
      { word: 'Interesting.', acts: ['Genuinely','Politely disagreeing','Bored','Suspicious','Impressed','Sarcastic','Distracted','Truly intrigued'] },
      { word: 'Let me check.', acts: ['Helpful','Buying time','Annoyed','Nervous','Confident','Distracted','Very polite','Worried'] },
      { word: 'That is a good question.', acts: ['Impressed','Stalling','Annoyed','Genuinely curious','To a child','Nervous','Amused','Brushing it off'] },
    ]
  },
  school: {
    label: 'At school',
    desc: 'Works as a classroom warm-up. Easy lines, big reactions.',
    list: [
      { word: 'I know.', acts: ['Confident','Annoyed','Desperate to answer','Bluffing','Bored','Quietly hurt','Warmly agreeing','Sarcastic'] },
      { word: 'Can I?', acts: ['Shy','Excited','Begging','Testing the limits','Polite','Impatient','Worried','Up to something'] },
      { word: 'My bad.', acts: ['Sincere','Joking','Embarrassed','Not sorry','In a rush','To a teacher','To a friend','The same mistake again'] },
      { word: 'Done!', acts: ['Proud','Relieved','Exhausted','Surprised it worked','In a rush','Disappointed','Showing off','Matter of fact'] },
    ]
  },
  party: {
    label: 'Party',
    desc: 'Loud rooms, big groups. The lines everyone already says.',
    list: [
      { word: 'Cheers!', acts: ['Loud and happy','Quiet','Formal','A farewell','A reunion','Exhausted','To a stranger','Celebrating big news'] },
      { word: 'No way!', acts: ['Disbelief','Excited','Horrified','Joking','Refusing flatly','Impressed','Suspicious','Dreading it'] },
      { word: 'Seriously?', acts: ['Shocked','Annoyed','Delighted','Doubtful','Worried','Joking','Disgusted','Impressed'] },
      { word: 'Same.', acts: ['Relating deeply','Casual','Joking','Half listening','Relieved','Embarrassed','Enthusiastic','Too tired to explain'] },
      { word: 'Oh my god.', acts: ['Shocked','Delighted','Horrified','Embarrassed','Annoyed','Moved','Joking','Completely drained'] },
    ]
  },
  faceonly: {
    label: 'No words',
    desc: 'Hard mode. Your face has to do all of it.',
    list: [
      { word: '(silence)', acts: ['You saw something you should not have','Tasting something delicious','Too sleepy to speak','Suddenly remembering','Holding in laughter','Not convinced','Deeply moved','Extremely nervous'] },
      { word: '(just a nod)', acts: ['Full agreement','Not listening','Reluctant','Still thinking','Happy','Giving up','In a hurry','Hiding something'] },
      { word: '(just a laugh)', acts: ['Genuine','Polite','Nervous','Cannot stop','Disbelieving','Shy','Mischievous','Laughing through tears'] },
      { word: '(just a sigh)', acts: ['Exhausted','Relieved','Exasperated','Moved','Bored','The tension just broke','Torn','Holding back anger'] },
    ]
  },
  family: {
    label: 'At home',
    desc: 'What gets said in every house, every single day.',
    list: [
      { word: 'Dinner!', acts: ['Calling everyone','Impatient','Asking what it is','Too tired to cook','Excited','It has gone cold','To the dog','Asking for the third time'] },
      { word: 'I am home.', acts: ['Exhausted','Happy','Sneaking in','Still angry','Half asleep','A child bursting in','Apologetic','Just routine'] },
      { word: 'Later.', acts: ['Putting it off','Gently','A real promise','Dodging the question','Annoyed','In a hurry','Looking forward to it','A soft no'] },
      { word: 'No.', acts: ['Firm','Gentle','Troubled','Embarrassed','Joking','Given up','Worried','Angry'] },
    ]
  },
  feelings: {
    label: 'Feelings',
    desc: 'Where the words say one thing and the voice says another.',
    list: [
      { word: 'Nothing.', acts: ['Truly nothing','Angry','Embarrassed','Sulking','Not interested','Very much something','Covering it up','Sad'] },
      { word: 'Maybe.', acts: ['Unsure','Hopeful','Genuinely torn','Testing them','Not interested','Shy','Worried','Secretly excited'] },
      { word: 'I like it.', acts: ['A confession','Shy','Casual','About food','Sincere','Covering up','As a joke','Working up the courage'] },
      { word: 'Whatever.', acts: ['Dismissive','Quietly hurt','Joking','Exhausted','Angry','Genuinely fine with it','Sulking','Defeated'] },
    ]
  },
  kids: {
    label: 'Kids',
    desc: 'Short words that younger players can read and act out.',
    list: [
      { word: 'No!', acts: ['Total refusal','Playful','Shy','Scared','Sleepy','Angry','Joking','Troubled'] },
      { word: 'Look!', acts: ['Showing off','Asking for help','Surprised','Delighted','Scared','Sharing a secret','In a hurry','Sulking'] },
      { word: 'I did it!', acts: ['Triumphant','Finally','Shy','Showing off','Relieved','Surprised at yourself','Matter of fact','Not what you expected'] },
      { word: 'Again!', acts: ['Begging','Angry','Delighted','Not convinced','Sleepy','Shy','Wanting to check','One last time'] },
      { word: 'Ouch.', acts: ['Real pain','Exaggerating','Holding it in','It hurt your feelings','Ticklish','Startled','Wanting attention','Cannot hold it back'] },
    ]
  },
};
