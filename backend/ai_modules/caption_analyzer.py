
# -----------------------------------
# CAPTION ANALYZER
# No ollama dependency — uses Groq
# -----------------------------------
 
# Stopwords to filter out
STOPWORDS = {
    "the","and","for","are","but","not","you","all","can","her","was","one",
    "our","out","day","get","has","him","his","how","its","let","may","new",
    "now","old","see","two","way","who","did","man","too","any","your","this",
    "with","have","from","they","will","been","when","what","that","then",
    "than","were","into","more","also","just","like","over","such","even",
    "most","some","well","here","each","does","very","only","made","said",
    "after","these","those","could","about","would"
}
 
# keyword → emotion/category mapping
KEYWORD_EMOTION_MAP = {
    "motivation": "motivational", "motivational": "motivational",
    "inspire":    "motivational", "success":      "motivational",
    "hustle":     "motivational", "grind":        "motivational",
    "happy":      "happy",        "joy":          "happy",
    "smile":      "happy",        "fun":          "happy",
    "celebrate":  "happy",
    "sad":        "sad",          "miss":         "sad",
    "alone":      "sad",          "heartbreak":   "sad",
    "pain":       "sad",
    "love":       "romantic",     "couple":       "romantic",
    "romantic":   "romantic",     "together":     "romantic",
    "travel":     "travel",       "trip":         "travel",
    "vacation":   "travel",       "explore":      "travel",
    "fitness":    "fitness",      "gym":          "fitness",
    "workout":    "fitness",      "training":     "fitness",
    "food":       "food",         "recipe":       "food",
    "cooking":    "food",         "delicious":    "food",
    "fashion":    "fashion",      "style":        "fashion",
    "outfit":     "fashion",      "ootd":         "fashion",
    "cricket":    "sports",       "football":     "sports",
    "sports":     "sports",       "ipl":          "sports",
    "tech":       "technology",   "coding":       "technology",
    "ai":         "technology",   "gadget":       "technology",
}
 
 
def analyze_caption(caption):
 
    if not caption or not caption.strip():
        return {
            "original_caption": "",
            "keywords":         [],
            "emotion":          "general",
            "caption_length":   0,
            "word_count":       0,
            "has_hashtags":     False,
            "has_emojis":       False,
            "caption_quality":  "No caption provided",
        }
 
    text = caption.strip()
 
    # -----------------------------------
    # EXTRACT MEANINGFUL KEYWORDS
    # -----------------------------------
 
    words = text.lower().replace("\n", " ").split()
 
    keywords = []
    for word in words:
        clean = word.strip(".,!?#@\"'()")
        if len(clean) > 3 and clean not in STOPWORDS and clean.isalpha():
            keywords.append(clean)
 
    # deduplicate keeping order
    seen = set()
    unique_keywords = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique_keywords.append(k)
 
    # -----------------------------------
    # DETECT EMOTION / CATEGORY
    # -----------------------------------
 
    emotion = "general"
    for kw in unique_keywords:
        if kw in KEYWORD_EMOTION_MAP:
            emotion = KEYWORD_EMOTION_MAP[kw]
            break
 
    # also check full caption text
    if emotion == "general":
        caption_lower = text.lower()
        for kw, emo in KEYWORD_EMOTION_MAP.items():
            if kw in caption_lower:
                emotion = emo
                break
 
    # -----------------------------------
    # CAPTION QUALITY RATING
    # -----------------------------------
 
    word_count    = len(words)
    has_hashtags  = "#" in text
    has_emojis    = any(ord(c) > 127 for c in text)
 
    if word_count >= 10 and has_hashtags and has_emojis:
        quality = "Excellent"
    elif word_count >= 5 and (has_hashtags or has_emojis):
        quality = "Good"
    elif word_count >= 3:
        quality = "Average"
    else:
        quality = "Too short — add more context"
 
    return {
        "original_caption": text,
        "keywords":         unique_keywords[:5],
        "emotion":          emotion,
        "caption_length":   len(text),
        "word_count":       word_count,
        "has_hashtags":     has_hashtags,
        "has_emojis":       has_emojis,
        "caption_quality":  quality,
    }
 