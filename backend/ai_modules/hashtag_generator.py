
# -----------------------------------
# HASHTAG GENERATOR
# Real hashtags based on user input
# -----------------------------------
 
HASHTAG_DB = {
    "fashion":     ["#Fashion", "#Style", "#OOTD", "#OutfitOfTheDay", "#FashionReels",
                    "#InstaFashion", "#Streetwear", "#FashionBlogger", "#Outfitcheck", "#StyleInspo"],
    "fitness":     ["#Fitness", "#Gym", "#Workout", "#FitnessMotivation", "#FitLife",
                    "#GymLife", "#BodyTransformation", "#FitnessJourney", "#WorkoutReels", "#Gains"],
    "motivation":  ["#Motivation", "#Success", "#Mindset", "#Discipline", "#GrowthMindset",
                    "#DailyMotivation", "#Hustle", "#Goals", "#PositiveVibes", "#Inspire"],
    "food":        ["#Foodie", "#FoodReels", "#InstaFood", "#Yummy", "#FoodPhotography",
                    "#FoodLovers", "#HomeCooking", "#Delicious", "#FoodBlogger", "#Recipe"],
    "travel":      ["#Travel", "#TravelGram", "#Wanderlust", "#Explore", "#TravelReels",
                    "#Adventure", "#HiddenGems", "#TravelLife", "#SoloTravel", "#Backpacking"],
    "sports":      ["#Sports", "#Cricket", "#Football", "#IPL", "#SportsMotivation",
                    "#Athletes", "#SportsReels", "#GameDay", "#Champion", "#Winning"],
    "technology":  ["#Tech", "#AI", "#Technology", "#Gadgets", "#Innovation",
                    "#TechReels", "#Coding", "#Programming", "#FutureTech", "#TechTok"],
    "romantic":    ["#Love", "#Couple", "#Romance", "#Relationship", "#CoupleGoals",
                    "#LoveStory", "#Together", "#Soulmate", "#CoupleReels", "#Valentines"],
    "sad":         ["#Feelings", "#Emotions", "#MentalHealth", "#SelfLove", "#Healing",
                    "#Overthinking", "#Relatable", "#EmotionalReels", "#FeelingsCheck"],
    "happy":       ["#Happy", "#Smile", "#Joy", "#GoodVibes", "#Positivity",
                    "#HappyLife", "#Blessed", "#Grateful", "#Happiness", "#Vibes"],
    "pet":         ["#PetLover", "#CutePets", "#DogLovers", "#CatLovers", "#PetsOfInstagram",
                    "#FurBaby", "#PetReels", "#DogsOfInstagram", "#CatsOfInstagram"],
    "entertainment":["#Entertainment", "#Movies", "#Comedy", "#Memes", "#WebSeries",
                    "#Bollywood", "#Hollywood", "#Reels", "#Funny", "#LOL"],
    "general":     ["#Trending", "#Viral", "#ExplorePage", "#FYP", "#Reels",
                    "#Instagram", "#ReelsIndia", "#ForYou", "#ViralReels", "#Explore"],
}
 
# Region-specific hashtags
REGION_HASHTAGS = {
    "IN": ["#India", "#IndianCreator", "#ReelsIndia", "#BollywoodVibes", "#DesiVibes"],
    "US": ["#USA", "#AmericanCreator", "#USTrends", "#ForYouPage"],
    "GB": ["#UK", "#BritishCreator", "#UKTrends"],
    "AU": ["#Australia", "#AussieCreator"],
}
 
# Content type → hashtag category
CONTENT_TO_HASHTAG = {
    "Human / Lifestyle Content":        "general",
    "Professional / Business Content":  "motivation",
    "Fitness Content":                  "fitness",
    "Food & Lifestyle Content":         "food",
    "Food Content":                     "food",
    "Sports Content":                   "sports",
    "Technology Content":               "technology",
    "Music / Entertainment Content":    "entertainment",
    "Travel Content":                   "travel",
    "Pet / Animal Content":             "pet",
    "Automobile Content":               "general",
    "General Viral Content":            "general",
}
 
 
def generate_hashtags(visual_data, caption_data, trend_data, region="IN"):
 
    hashtags = []
 
    content_type     = visual_data.get("content_type", "General Viral Content")
    # Use primary_category from visual analysis — most accurate
    primary_category = visual_data.get("primary_category", "lifestyle")
    keywords         = caption_data.get("keywords", [])
    emotion          = caption_data.get("emotion", "general")
    trend_tags       = trend_data.get("hashtags", [])
    caption_text     = caption_data.get("original_caption", "").lower()
 
    # map primary_category to hashtag category
    VISUAL_TO_HASHTAG = {
        "food":"food","sports":"sports","fitness":"fitness","fashion":"fashion",
        "technology":"technology","travel":"travel","automobile":"general",
        "pet":"pet","nature":"travel","entertainment":"entertainment",
        "education":"general","business":"motivation","lifestyle":"general",
        "motivation":"motivation","romantic":"romantic","sad":"sad","happy":"happy",
    }
    category = VISUAL_TO_HASHTAG.get(primary_category, "general")
 
    for kw in keywords:
        tag = f"#{kw.strip().capitalize()}"
        if tag not in hashtags:
            hashtags.append(tag)
 
    # also extract hashtags already in caption
    for word in caption_text.split():
        if word.startswith("#") and len(word) > 2:
            tag = word.capitalize()
            if tag not in hashtags:
                hashtags.append(tag)
 
    # -----------------------------------
    # 2. EMOTION-BASED HASHTAGS
    # -----------------------------------
 
    emotion_tags = HASHTAG_DB.get(emotion, [])
    for tag in emotion_tags[:5]:
        if tag not in hashtags:
            hashtags.append(tag)
 
    # 3. VISUAL CATEGORY HASHTAGS
    content_tags = HASHTAG_DB.get(category, HASHTAG_DB["general"])
    for tag in content_tags[:5]:
        if tag not in hashtags:
            hashtags.append(tag)
 
    # -----------------------------------
    # 4. LIVE TREND HASHTAGS
    # From Google Trends / pytrends
    # -----------------------------------
 
    for tag in trend_tags[:5]:
        if tag not in hashtags:
            hashtags.append(tag)
 
    # -----------------------------------
    # 5. REGION HASHTAGS
    # -----------------------------------
 
    region_tags = REGION_HASHTAGS.get(region, REGION_HASHTAGS["IN"])
    for tag in region_tags[:2]:
        if tag not in hashtags:
            hashtags.append(tag)
 
    # -----------------------------------
    # 6. ALWAYS ADD CORE VIRAL TAGS
    # -----------------------------------
 
    for tag in ["#Trending", "#Viral", "#ExplorePage", "#FYP", "#Reels"]:
        if tag not in hashtags:
            hashtags.append(tag)
 
    # -----------------------------------
    # CATEGORIZE INTO TIERS
    # -----------------------------------
 
    viral_tags = [t for t in hashtags if t in ["#Trending","#Viral","#FYP","#ExplorePage","#Reels","#ForYou"]]
    niche_tags = [t for t in hashtags if t in emotion_tags or t in content_tags]
    safe_tags  = [t for t in hashtags if t not in viral_tags and t not in niche_tags]
 
    # final list — max 18
    final_hashtags = list(dict.fromkeys(hashtags))[:18]
 
    # -----------------------------------
    # ALGORITHM BOOST RATING
    # -----------------------------------
 
    boost = "High" if len(keywords) >= 2 and emotion != "general" else "Medium"
 
    return {
        "recommended_hashtags": final_hashtags,
        "viral_hashtags":       viral_tags[:5],
        "niche_hashtags":       niche_tags[:5],
        "hashtag_count":        len(final_hashtags),
        "hashtag_strategy": {
            "best_count":       "12-18 hashtags",
            "best_mix":         "Keyword + Niche + Viral + Region",
            "algorithm_boost":  boost,
        }
    }
 
 
# compatibility alias
def generate_smart_hashtags(visual_data, caption_data, trend_data):
    return generate_hashtags(visual_data, caption_data, trend_data)