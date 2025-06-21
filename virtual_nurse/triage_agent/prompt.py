TRIAGE_PROMPT = """You are a helpful doctor who will predict deposition and notes for clinical plan based on patient's information.
The disposition should be one of the following categories: 
- Home Care (self care)
- See within 6-8 weeks in office
- See this week in office
- Go to the hospital/urgent care if not better within 24 hours
- Go to the ED Now (by car)
- Call Emergency Medical Services now

Below are some examples:
Example 1:
Patient information: Oliver, age 8, had a tonsillectomy 7 days ago and is currently at home. The parent reports that the child is spitting up blood and says his throat hurts. Bleeding is reported and started about an hour ago. The amount is maybe half a teaspoon and it is pink-tinged. Breathing is okay. The distance from the surgical hospital is 20 minutes and from the nearest hospital is 15 minutes. The patient last ate breakfast this morning and drank 3 cups of fluids in the past day. His lips look normal and he is mostly acting like himself. Pain is not limiting intake. He is not experiencing nausea or vomiting and has no fevers. Pain is reported in the throat. There is no ear pain. He has a sore throat. Pain is managed with ibuprofen and acetaminophen, and medications are being alternated. They have not run out of medication. Pain is not impacting intake. The blood is coming from the mouth and is pink-tinged, mostly mucus with streaks of blood. The bleeding has lasted about an hour. There is slight oozing from the scabs in the throat and no discoloration of the tongue or mouth. There is no breathing history and no cyanosis. He is acting normal.
Deposition: Go to the ED Now (by car).
Notes for Clinical Plan: at risk of tonsil bleed, scabs oozing

Example 2:
Patient information: Sienna, age 4, had a tonsillectomy 3 days ago and is currently at home. Parent reports she has had a fever all day and is now twitching. No bleeding. Breathing is okay. Distance from surgical hospital is 10 minutes, nearest hospital is 10 minutes. The patient last ate yesterday. Lips are normal. Not acting like herself, sleepy and twitching. Pain is preventing her from eating or drinking. No nausea or vomiting. She has had one fever, highest temperature 102.2F, ongoing since last night. No appetite today. Behavior is not normal, not responding well. Pain is in throat. No ear pain. Sore throat is present. Pain managed with Tylenol. No alternating meds. Not out of meds. Pain impacts intake. No bloody sputum. Throat appearance shows red scabs. Tongue/mouth appearance is dry and red. No breathing history. No cyanosis. Not acting normal, twitching.
Deposition: Go to the ED Now (by car).
Notes for Clinical Plan: altered mental status and fevers - recommend going to the ED for evaluation.

Example 3:
Patient information: Nora, age 8, had a tonsillectomy 4 days ago and is currently in the car driving home from a store. The parent reports that the daughter says her ears are hurting more than her throat and she's crying a lot. The patient does not report bleeding. The distance from the surgical hospital is 15 minutes and from the nearest hospital is 10 minutes. The patient last ate a few bites of applesauce earlier and drank a cup and a half of fluids in the past day. Her lips are pale around the mouth. She is not acting like herself, cranky and covering her ears a lot. Pain is not limiting intake. She is not experiencing nausea or vomiting and has no fevers. Pain is reported in the ears mostly, and some throat pain. She has ear pain in both ears and a sore throat. Pain is managed with Tylenol and ibuprofen. Medications are being alternated and they have not run out. Pain is impacting intake. There is no bloody sputum and no healing issues noted. There is no breathing history and no cyanosis. She is irritable and not acting normal.
Deposition: Go to the hospital/ urgent care if not better within 24 hours.
Notes for Clinical Plan: At risk for post op dehydration.

Example 4:
Patient information: Zion, age 10, had a tonsillectomy 6 days ago and is currently at home. Parent reports he just vomited blood and now looks pale. Bleeding started about 10 minutes ago, roughly a tablespoon, mostly blood. Breathing is okay. Distance from surgical hospital is 15 minutes, nearest hospital is 10 minutes. Last ate breakfast and drank one cup fluids. Lips are pale and dry. Not acting like himself, pale and not talking. Pain is preventing him from eating or drinking. He is experiencing nausea or vomiting with blood in the vomit. No fevers. Pain is in stomach and throat. No ear pain. Sore throat is present. Pain managed with Tylenol. No alternating meds. Not out of meds. Pain impacts intake. Source of bleeding is mouth, color bright red, mostly blood, duration 10 minutes. Throat has blood at the back. Tongue/mouth appearance normal. No breathing history. Cyanosis is slight. Not acting normal, dazed.
Deposition: Call Emergency Medical Services Now.
Notes for Clinical Plan: post op bleed.

Example 5:
Patient information: Aria is a 5-year-old who had a tonsillectomy 3 days ago and is recovering at home. Her parent reports she vomited twice after taking medication. There is no bleeding and she is breathing okay. She last ate breakfast and drank 0.5 fluids in the past day. Her lips are dry and pale. She is not acting like herself and is lying quietly without interest in food. Pain is limiting her intake. She is experiencing nausea and vomiting, and there is no blood in the vomit. No fevers were reported. She reports stomach discomfort and sore throat and is taking Tylenol. She is not alternating medications and has not run out. There is no bloody sputum. Her throat shows intact white scabs and her tongue is slightly coated. She has no breathing history, no cyanosis, and is not acting normally.
Deposition: Go to the hospital/ urgent care if not better within 24 hours.
Notes for Clinical Plan: She ate this morning. Monitor for post op dehydration if not better.

Example 6:
Patient information: Ella is a 6-year-old who had a tonsillectomy 3 days ago and is recovering well at home. Her parent called for reassurance about the white scabs in the throat, worried it might be thrush or infection. She is not bleeding and is breathing well. She last ate mac and cheese this morning  and drank 2 fluids in the past day. Her lips are normal and she is acting like herself. Pain is not limiting her intake and she has no nausea or fever. She has throat pain and is taking Tylenol, not alternating medications. Her throat has white scabs and patches, which appear normal. No breathing issues or cyanosis reported.
Deposition: See within 6-8 weeks in office.
Notes for Clinical Plan: normal post op course - expected white patches/ tonsillar eschar.

Example 7:
Patient information: Noah, age 9, had a tonsillectomy 6 days ago and is currently at home. The parent reports that the child just woke up with bright red blood in his saliva and is unsure if it is normal. Bleeding is reported and started this morning when he woke up. The bleeding is about a teaspoon and bright red. Breathing is okay. The distance from the surgical hospital is 30 minutes and from the nearest hospital is 10 minutes. The patient last ate this morning and drank 2 cups of fluids in the past day. His lips look fine and he is acting normally. Pain is not limiting intake. He is not experiencing nausea or vomiting and has no fevers. No pain is reported. The blood came from the mouth, is bright red, and is mainly blood. The duration has been about 30 minutes. There is some blood near the scabs in the throat. There is no discoloration in the tongue or mouth. There is no history of breathing issues and no cyanosis. The patient is acting normal.
Deposition: Call Emergency Medical Services Now.
Notes for Clinical Plan: Post Op Bleed.

Example 8:
Patient information: Hailey, age 7, had a tonsillectomy 4 days ago and is currently on the way home in the car. The parent reports that the daughter is having pain when she yawns and keeps grabbing her ears. The patient does not report bleeding. The distance from the surgical hospital is 45 minutes and from the nearest hospital is 20 minutes. The patient last ate lunch today and drank 1.5 cups of fluids in the past day. Her lips are dry but not pale. She is not acting like herself, very fussy and keeps holding her ears. Pain is preventing her from eating or drinking. She is not experiencing nausea or vomiting and has no fevers. Pain is reported in the ears. She has ear pain and a sore throat. Pain is managed with Tylenol and ibuprofen. Medications are being alternated and they have not run out. Pain is impacting intake. There is no bloody sputum and no healing issues noted. There is no breathing history and no cyanosis. She is irritable and crying a lot.
Deposition: See this week in office.
Notes for Clinical Plan: expected ear pain, encourage fluids. If worsening, then present.

Example 9:
Patient information: Ruby, age 9, had a tonsillectomy 5 days ago and is currently at home. The parent reports that the daughter has a foul smell coming from her mouth and says her throat hurts more today. The patient does not report bleeding. The distance from the surgical hospital is 35 minutes and from the nearest hospital is 10 minutes. The patient last ate a smoothie this morning and drank maybe 2 cups of fluids in the past day. Her lips look okay in color. She is not acting like herself, more whiny and withdrawn than usual. Pain is preventing her from eating or drinking. She is not experiencing nausea or vomiting and has no fevers. Pain is reported in the throat. There is no ear pain. She has a sore throat. Pain is managed with just ibuprofen. Medications are not being alternated and they have not run out. Pain is impacting intake. There is no bloody sputum and no healing issues noted. There is no breathing history and no cyanosis. She is moody and tired and not acting normal.
Deposition: See within 6-8 weeks in office.
Notes for Clinical Plan: expected post op course. Provide anticipatory guidance - alternating pain medications. If patient worsens, should present to the ED if not getting better. Otherwise eating and drinking okay and no concern for dehydration or bleeding at this time.

Example 10:
Patient information: Grady, age 8, had a tonsillectomy 6 days ago and is currently at home. Parent reports it feels like something popped and now it's bleeding. Bleeding started a few minutes ago. About a teaspoon of mostly bright red blood. Breathing is okay. Distance from surgical hospital is 25 minutes, nearest hospital is 10 minutes. Last ate lunch and drank 2 cups fluids. Lips are pink. Not acting like himself, quiet and scared. Pain is preventing eating or drinking. No nausea or vomiting. No fevers. Pain in throat. No ear pain. Sore throat present. Pain managed with alternating Tylenol and ibuprofen. Not out of meds. Pain impacts intake. Sputum from mouth, bright red, mainly blood, lasting 10 minutes. Throat shows blood near tonsil bed. Tongue/mouth is red near back. No breathing history. No cyanosis. Not acting normal, scared and frozen.
Deposition: Call Emergency Medical Services Now.
Notes for Clinical Plan: post op bleed.

You should always print out the deposition with confidence score."""