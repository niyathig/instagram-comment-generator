#!/usr/bin/env python3
"""Generate 600 realistic synthetic Instagram comments without dataset download"""

import json
import random
import os

# Synthetic captions (representative of Instagram content)
synthetic_captions = [
    "Morning coffee vibes ☕", "Golden hour energy ✨", "Sunset chasing",
    "Beach day with the squad", "Friday night plans", "Self care Sunday",
    "Obsessed with this place 🌴", "NYC state of mind", "Hiking adventure",
    "Favorite people in one photo", "Fresh start", "Living my best life",
    "Grateful for moments like these", "That glow up though", "Spa day needed",
    "Brunch is the best meal", "Current mood", "Literally can't even",
    "Make it happen", "Growth over perfection", "Simple pleasures",
    "Date night 💕", "Squad goals", "New outfit alert", "Hair progress",
    "Workout done ✅", "Meal prep Sunday", "Netflix and chill", "Study session",
    "Concert vibes", "Festival season", "Road trip energy", "City lights",
    "Rainy day mood", "Snow day magic", "Spring flowers", "Fall leaves",
    "Winter wonderland", "Summer nights", "Paradise found", "Dream destination",
    "Goals achieved", "Manifesting", "Gratitude journal", "Mindful moments",
    "Mental health matters", "Self love", "Positive vibes only", "Living legend",
    "Creative process", "Art therapy", "Music to my ears", "Bookworm life",
    "Coffee addict", "Foodie adventures", "Cooking at home", "Baking therapy",
    "Farmer's market haul", "Farm to table", "Organic vibes", "Green smoothie",
    "Cheat day allowed", "Guilty pleasure", "Sweet tooth", "Dessert goals",
    "Pizza night", "Taco Tuesday", "Sushi obsessed", "Pasta dreams",
    "Bubble tea runs", "Latte art", "Espresso shots", "Cold brew",
    "Puppy love 🐶", "Cat mom life", "Pet parent", "Animal lover",
    "Dog day care", "Furry friends", "Paws and love", "Cuddle buddies",
    "New puppy alert", "Growing up fast", "Best friends forever", "Besties",
    "Ride or die", "Found my people", "Chosen family", "Tribe vibes",
    "Friendship goals", "Laughing so hard", "Inside jokes", "Remember when",
    "Throwback to", "Memories made", "Making moments count", "Forever grateful",
    "Family time", "Siblings goals", "Parent love", "Generational blessing",
    "Home sweet home", "Dream house", "New apartment", "Cozy corner",
    "Interior goals", "Decor inspo", "Plant parent", "Green thumb",
    "Gardening season", "Succulent collection", "Flower child", "Blooming",
    "Fashion forward", "Style inspiration", "Outfit of the day", "Thrifted finds",
    "Fast fashion detox", "Capsule wardrobe", "Designer dupe", "Budget friendly",
    "Sustainable fashion", "Eco conscious", "Zero waste goals", "Plastic free",
    "Reusable everything", "Mother earth", "Save the planet", "Climate action",
    "Activist life", "Cause driven", "Giving back", "Volunteer work",
    "Community service", "Make a difference", "Change maker", "World changer",
    "Education matters", "Student life", "Graduation day", "New job alert",
    "Career goals", "Crushing it", "Promoted", "Side hustle", "Entrepreneur life",
    "Boss moves", "Building empire", "Success mindset", "Wealth creation",
    "Financial freedom", "Investment journey", "Passive income", "Money goals",
    "Abundance mindset", "Prosperity consciousness", "Manifesting wealth", "Rich life",
    "Luxury vibes", "High maintenance low key", "Bougie", "Living large",
    "Travel goals", "Bucket list", "Passport ready", "Jet setter", "Nomad life",
    "Wanderlust", "Adventure awaits", "Exploration mode", "Discovery", "New culture",
    "International travel", "Visa runs", "Travel blog", "Instagram tourism",
    "Hidden gems", "Local experience", "Off the beaten path", "Secret spots",
    "Tourist trap avoided", "Authentic vibes", "Real travel", "Getting lost",
    "Maps optional", "No plans best plans", "Spontaneous trip", "Last minute",
    "YOLO energy", "Live for today", "Carpe diem", "No regrets", "Risk taker",
    "Thrill seeker", "Adrenaline junkie", "Extreme sports", "Bucket list item",
    "Checked off", "Achievement unlocked", "Level up", "New record", "Personal best",
    "Fitness goals", "Gym progress", "Gains", "Shred season", "Get fit", "Stay healthy",
    "Wellness journey", "Mental clarity", "Peace of mind", "Zen life", "Yoga practice",
    "Meditation mode", "Chakra alignment", "Crystal healing", "Spiritual awakening",
    "Universe alignment", "Cosmic connection", "Star child", "Old soul", "Reincarnation",
    "Past life recall", "Metaphysical", "Alternative medicine", "Holistic health",
    "Natural remedy", "Essential oils", "Ayurvedic", "TCM", "Acupuncture",
    "Massage therapy", "Self healing", "Energy work", "Sound healing", "Vibration",
    "Frequency", "Numerology", "Astrology", "Moon cycle", "Eclipse energy",
    "Mercury retrograde", "Saturn return", "Venus transit", "Mars energy", "Jupiter luck",
    "Pluto transformation", "Neptune dreams", "Uranus revolution", "Birth chart",
    "Zodiac sign", "Astro queen", "Cosmic queen", "Spiritual queen", "Priestess energy",
    "Light worker", "Indigo child", "Crystal child", "Rainbow child", "Starseed",
    "Ascending", "Fifth dimension", "Enlightenment", "Awakening", "Consciousness",
    "Higher self", "Twin flame", "Soul mate", "Soulmate connection", "Meant to be",
    "Fated meeting", "Synchronicity", "Universe brings", "Divine timing", "God's plan",
    "Blessed beyond measure", "Grateful everyday", "Count your blessings", "Thankful",
    "Appreciative", "Gratitude practice", "Blessing journal", "Abundance check",
    "Full circle moment", "Closure achieved", "Moving forward", "New chapter",
    "Life lesson", "Personal growth", "Character building", "Humble pie", "Lessons learned",
    "Wisdom gained", "Knowledge shared", "Teaching moment", "Learn from mistakes",
    "Growth mindset", "Never stop learning", "Constant student", "School of life",
    "Hard knock university", "Street smart", "Book smart", "Common sense", "Good instincts",
    "Trust your gut", "Intuition", "Third eye", "Inner knowing", "Gut feeling"
]

# Expand to 600+ captions with variations
expanded_captions = []
for caption in synthetic_captions:
    expanded_captions.append(caption)
    # Add variations
    if len(expanded_captions) < 600:
        expanded_captions.append(f"{caption} 🌟")
    if len(expanded_captions) < 600:
        expanded_captions.append(f"{caption}!")

# Trim to exactly 600
synthetic_captions = expanded_captions[:600]

# Comment generation templates
compliment_starters = [
    "omg", "wow", "you look", "literally", "okay but", "this is", "i love",
    "so", "such", "goals", "stunning", "obsessed", "literally obsessed",
    "this made", "can we", "we need", "let's", "absolutely", "10/10", "slay",
    "main character", "that glow", "come on now", "excuse me", "not you",
    "stop it", "the way", "i'm", "no but", "yes and"
]

compliment_enders = [
    "😍", "🔥", "💕", "✨", "😭", "🙌", "", "💫", "👑", "🌟", "💘", "😘",
    "always", "tho", "period", "bestie", "queen", "legend"
]

travel_starters = [
    "i need", "wish i was", "adding to", "been dying", "no but",
    "when can", "take me", "literally", "okay but", "this place", "here looks",
    "brb", "booking now", "passport ready", "see you soon", "manifesting"
]

travel_phrases = [
    "there", "to this place", "this badly", "to go back",
    "to explore here", "to be there", "asap", "immediately", "yesterday"
]

travel_enders = [
    "😭", "🙏", "✈️", "🌍", "💔", "", "asap", "pls", "soon", "🏖️", "🏔️"
]

food_starters = [
    "lol", "omg stop", "literally", "this looks", "excuse me", "why",
    "i'm", "okay", "can we", "this is", "no but", "send", "need", "where",
    "tag me", "see you soon", "coming thru"
]

food_enders = [
    "🍽️", "😍", "👀", "🤤", "", "rn", "lol", "🔥", "🤤", "periodt", "tho"
]

funny_starters = [
    "lol", "lmaooo", "wait", "hahaha", "literally", "same", "no but",
    "stop", "why", "okay but", "actually", "bestie no", "excuse me", "not me"
]

funny_enders = [
    "😂", "", "💀", "😭", "stop", "im dead", "lol", "bye", "💀💀💀", "screaming"
]

generic_comments = [
    "this is everything 🔥",
    "i love this so much",
    "goals 😭",
    "this made my day",
    "we need to do this",
    "lol same 😂",
    "stunning as always 💕",
    "obsessed 🙌",
    "yes yes yes ✨",
    "literally perfect",
    "save some talent for us 👑",
    "no but actually",
    "the way you—",
    "i'm speechless 😍",
    "this is art",
    "okay you're winning",
    "absolutely not okay 💔",
    "need this energy",
    "come thruuu",
    "main character energy",
    "periodt 💋",
    "facts only",
    "the vibes",
    "chef's kiss",
    "ate and left",
    "understood the assignment",
    "no notes",
    "it's the way for me",
    "i have no words",
    "perfectly imperfect",
    "raw talent",
    "unmatched energy",
    "the legend",
    "iconic",
    "timeless",
    "forever mood",
    "never getting over",
    "amen to that",
    "tag yourself",
    "real ones know"
]

def detect_context(caption):
    """Detect caption context to vary comment type"""
    caption_lower = caption.lower()

    person_keywords = ["me", "i'm", "myself", "face", "smile", "eyes", "look",
                      "hair", "outfit", "dress", "fit", "selfie", "photo", "pic", "glow"]

    travel_keywords = ["beach", "city", "travel", "trip", "vacation", "adventure",
                      "mountains", "lake", "hotel", "airport", "flight", "nyc", "la",
                      "paris", "tokyo", "london", "dubai", "exploring", "wandering",
                      "paradise", "destination", "passport", "jet", "nomad", "wanderlust"]

    food_keywords = ["food", "eat", "coffee", "breakfast", "lunch", "dinner", "pizza",
                    "burger", "sushi", "cake", "dessert", "chocolate", "yum", "taste",
                    "restaurant", "cooking", "baking", "brunch", "latte", "smoothie"]

    animal_keywords = ["dog", "cat", "puppy", "kitten", "pet", "animal", "bird",
                      "horse", "bunny", "paws", "adorable", "cute", "fur", "furry"]

    event_keywords = ["party", "night out", "celebration", "event", "concert", "show",
                     "wedding", "birthday", "festival", "game", "club"]

    person_score = sum(1 for kw in person_keywords if kw in caption_lower)
    travel_score = sum(1 for kw in travel_keywords if kw in caption_lower)
    food_score = sum(1 for kw in food_keywords if kw in caption_lower)
    animal_score = sum(1 for kw in animal_keywords if kw in caption_lower)
    event_score = sum(1 for kw in event_keywords if kw in caption_lower)

    scores = {
        "person": person_score,
        "travel": travel_score,
        "food": food_score,
        "animal": animal_score,
        "event": event_score
    }

    max_score = max(scores.values())
    if max_score == 0:
        return "generic"

    return max(scores, key=scores.get)

def generate_comment(caption):
    """Generate a realistic Instagram comment for a caption"""
    context = detect_context(caption)

    # 35% chance of using a pre-written generic comment
    if random.random() < 0.35:
        return random.choice(generic_comments)

    # Context-specific comments
    if context == "person":
        starter = random.choice(compliment_starters)
        ender = random.choice(compliment_enders)
        phrases = ["look amazing", "are so cute", "never miss", "always killing it",
                  "are a vibe", "have my heart", "are the one", "slay", "serve looks"]
        phrase = random.choice(phrases)
        comment = f"{starter} {phrase} {ender}".strip()
        return comment[:100]

    elif context == "travel":
        starter = random.choice(travel_starters)
        phrase = random.choice(travel_phrases)
        ender = random.choice(travel_enders)
        comment = f"{starter} {phrase} {ender}".strip()
        return comment[:100]

    elif context == "food":
        starter = random.choice(food_starters)
        ender = random.choice(food_enders)
        phrases = ["look good right now", "need this", "smells amazing",
                  "would demolish this", "is calling my name", "i'm drooling"]
        phrase = random.choice(phrases)
        comment = f"{starter} {phrase} {ender}".strip()
        return comment[:100]

    elif context == "animal":
        starters = ["this is", "omg the", "look at", "i can't", "those", "so", "literally"]
        starter = random.choice(starters)
        enders = ["😍", "🥺", "💕", "😭", "🙌", ""]
        ender = random.choice(enders)
        phrases = ["cutest thing ever", "sweetest baby", "fluffiest", "precious",
                  "adorable i'm crying", "pure", "perfect angel"]
        phrase = random.choice(phrases)
        comment = f"{starter} {phrase} {ender}".strip()
        return comment[:100]

    elif context == "event":
        starter = random.choice(funny_starters)
        ender = random.choice(funny_enders)
        phrases = ["this looks lit", "what a night", "living for this energy",
                  "you're killing it", "this energy", "vibes only"]
        phrase = random.choice(phrases)
        comment = f"{starter} {phrase} {ender}".strip()
        return comment[:100]

    else:  # generic
        return random.choice(generic_comments)

# Generate comments
print("Generating 600 synthetic Instagram comments...\n")
results = []

for idx, caption in enumerate(synthetic_captions):
    comment = generate_comment(caption)
    results.append({
        "index": idx,
        "caption": caption,
        "comment": comment
    })

    if (idx + 1) % 50 == 0:
        print(f"✓ Generated {idx + 1}/600 comments")

# Save to file
output_path = os.path.expanduser("~/Desktop/synthetic_comments.json")
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n✓ Complete! Saved 600 comments to ~/Desktop/synthetic_comments.json")
print(f"\nSample comments:")
for i in random.sample(range(600), 5):
    print(f"  [{results[i]['index']}] Caption: {results[i]['caption']}")
    print(f"      Comment: {results[i]['comment']}\n")
