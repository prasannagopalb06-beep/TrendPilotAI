import time
import random
import requests
import os
from dotenv import load_dotenv
 
load_dotenv()
 
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
 
# -----------------------------------
# REGIONAL SONG DATABASE
# Real trending songs by region + category
# -----------------------------------
 
REGIONAL_SONGS = {
    "IN": {
        "motivation":  ["Kar Har Maidaan Fateh", "Zinda", "Dangal Theme", "Sultan Theme", "Bhaag Milkha Bhaag"],
        "fashion":     ["Hukum", "Arabic Kuthu", "Bijlee Bijlee", "Manike", "Jhoome Jo Pathaan"],
        "fitness":     ["Vaathi Coming", "Besharam Rang", "Believer", "Unstoppable", "Zinda"],
        "food":        ["Enjoy Enjaami", "Param Sundari", "Swag Se Swagat", "Naatu Naatu"],
        "travel":      ["Ilahi", "Safarnama", "Tum Ho", "Ik Vaari Aa", "Zindagi Na Milegi Dobara"],
        "romantic":    ["Kesariya", "Raataan Lambiyan", "Tum Hi Ho", "Munbe Vaa", "Adiye"],
        "sad":         ["Channa Mereya", "Ae Dil Hai Mushkil", "Tujhe Kitna Chahne Lage", "Life of Ram"],
        "sports":      ["Naatu Naatu", "Dangal", "Sultan", "Jag Ghoomeya", "Sooraj Dooba Hai"],
        "comedy":      ["Gallan Goodiyaan", "Saturday Saturday", "London Thumakda", "Desi Girl"],
        "technology":  ["Zinda", "Believer", "The Spectre", "Centuries", "Warriors"],
        "pet":         ["Sooraj Ki Baahon Mein", "Happy", "Cute", "Tum Se Hi"],
        "general":     ["Kesariya", "Naatu Naatu", "Hukum", "Vaathi Coming", "Jawan Theme"],
        "entertainment":["Jawan Theme", "Pathaan Title Track", "Pushpa Pushpa", "RRR Naatu Naatu"],
    },
    "TN": {  # Tamil Nadu
        "motivation":  ["Vaathi Coming", "Kannaana Kanney", "Naan Sirithal", "Rowdy Baby"],
        "fashion":     ["Hukum", "Arabic Kuthu", "Enjoy Enjaami", "Kannazhaga"],
        "fitness":     ["Vaathi Coming", "Survivor", "Rowdy Baby", "Aaluma Doluma"],
        "romantic":    ["Munbe Vaa", "Adiye", "Nee Kavithaigala", "Uyire", "Kaathuvaakula"],
        "sad":         ["Life of Ram", "Nee Kavithaigala", "Oru Murai", "Kaaney Kaaney"],
        "general":     ["Hukum", "Vaathi Coming", "Enjoy Enjaami", "Arabic Kuthu", "Rowdy Baby"],
    },
    "US": {
        "motivation":  ["Eye of the Tiger", "Hall of Fame", "Roar", "Titanium", "Unstoppable"],
        "fashion":     ["Industry Baby", "Bad Guy", "Levitating", "As It Was", "Flowers"],
        "fitness":     ["Till I Collapse", "Stronger", "Power", "Lose Yourself", "Jump"],
        "food":        ["Happy", "Good as Hell", "Can't Stop the Feeling", "Shake It Off"],
        "travel":      ["Life is a Highway", "Take Me Home Country Roads", "Wanderlust"],
        "romantic":    ["Perfect", "All of Me", "A Thousand Years", "Thinking Out Loud"],
        "sad":         ["Someone Like You", "Fix You", "The Night We Met", "Skinny Love"],
        "sports":      ["Eye of the Tiger", "We Will Rock You", "Jump Around", "Lose Yourself"],
        "comedy":      ["Happy", "Uptown Funk", "24K Magic", "Can't Stop the Feeling"],
        "technology":  ["Centuries", "Radioactive", "Warriors", "The Spectre"],
        "general":     ["As It Was", "Flowers", "Levitating", "Blinding Lights", "Stay"],
    },
    "GB": {
        "motivation":  ["Hall of Fame", "Roar", "Fight Song", "Stronger", "Eye of the Tiger"],
        "fashion":     ["As It Was", "Flowers", "Bad Guy", "Levitating", "Don't Start Now"],
        "general":     ["As It Was", "Flowers", "Blinding Lights", "Watermelon Sugar", "Levitating"],
        "romantic":    ["Perfect", "Shape of You", "Someone You Loved", "Before You Go"],
        "sad":         ["Fix You", "Someone Like You", "The Scientist", "Yellow"],
    },
}
 
# -----------------------------------
# REGIONAL HASHTAG DATABASE
# -----------------------------------
 
REGIONAL_HASHTAGS = {
    "IN": {
        "motivation":  ["#MotivationIndia", "#IndianMotivation", "#HindiMotivation", "#DesiHustle", "#IndianYouth"],
        "fashion":     ["#IndianFashion", "#DesiStyle", "#BollywoodFashion", "#IndianOOTD", "#DesiGirl"],
        "fitness":     ["#IndianFitness", "#DesiGym", "#FitIndia", "#IndianBodybuilding", "#DesiWorkout"],
        "food":        ["#IndianFood", "#DesiFood", "#StreetFoodIndia", "#IndianCooking", "#FoodiesOfIndia"],
        "travel":      ["#IncredibleIndia", "#TravelIndia", "#IndianTravel", "#ExploreBharat", "#IndiaTravel"],
        "sports":      ["#IPL", "#Cricket", "#IndianCricket", "#BCCI", "#CricketIndia"],
        "entertainment":["#Bollywood", "#BollywoodReels", "#HindiReels", "#BollywoodVibes", "#IndianCinema"],
        "general":     ["#India", "#IndianCreator", "#ReelsIndia", "#DesiVibes", "#BharatReels"],
    },
    "TN": {
        "general":     ["#TamilReels", "#TamilContent", "#TamilCreator", "#Kollywood", "#TamilPonnu"],
        "motivation":  ["#TamilMotivation", "#TamilHustle", "#TamilYouth"],
        "fashion":     ["#TamilFashion", "#TamilStyle", "#KollywoodFashion"],
        "food":        ["#TamilFood", "#ChennaiFood", "#TamilCooking", "#Samayal"],
        "entertainment":["#Kollywood", "#TamilCinema", "#Vijay", "#Ajith", "#TamilMovies"],
    },
    "US": {
        "general":     ["#USA", "#AmericanCreator", "#USAReels", "#ForYouPage", "#AmericanLife"],
        "motivation":  ["#AmericanDream", "#HustleCulture", "#USAMotivation"],
        "fashion":     ["#NYCFashion", "#USFashion", "#AmericanStyle", "#StreetStyleUSA"],
        "food":        ["#AmericanFood", "#USAFood", "#FoodieUSA", "#AmericanEats"],
    },
    "GB": {
        "general":     ["#UK", "#BritishCreator", "#UKReels", "#BritishLife", "#LondonLife"],
        "fashion":     ["#LondonFashion", "#UKStyle", "#BritishFashion"],
        "food":        ["#BritishFood", "#UKFoodie", "#LondonEats"],
    },
}
 
# -----------------------------------
# FALLBACK TREND DATABASE
# -----------------------------------
 
TREND_DATABASE = {
    "fashion":     {"trending_topics":["Street Fashion","OOTD Reels","Celebrity Looks","Fashion Week","Thrift Flip"],
                    "viral_hashtags":["#Fashion","#OOTD","#Style","#FashionReels","#Outfitcheck"]},
    "motivation":  {"trending_topics":["Morning Routine","Success Stories","Mindset Shift","Daily Habits","Glow Up"],
                    "viral_hashtags":["#Motivation","#Mindset","#Success","#GlowUp","#DailyHabits"]},
    "travel":      {"trending_topics":["Hidden Places","Budget Travel","Nature Reels","Solo Travel","Travel Hacks"],
                    "viral_hashtags":["#Travel","#Wanderlust","#TravelGram","#Explore","#HiddenGems"]},
    "fitness":     {"trending_topics":["Gym Motivation","Workout Reels","Transformation","Home Workout","Calisthenics"],
                    "viral_hashtags":["#Fitness","#Gym","#Workout","#FitnessMotivation","#BodyTransformation"]},
    "food":        {"trending_topics":["Street Food","Food Reviews","Cooking Shorts","Food Challenges","Recipe Reels"],
                    "viral_hashtags":["#Foodie","#FoodReels","#InstaFood","#Yummy","#FoodLovers"]},
    "technology":  {"trending_topics":["AI Tools","Tech Reviews","Gadget Unboxing","Life Hacks","Coding Tips"],
                    "viral_hashtags":["#Tech","#AI","#Gadgets","#TechTok","#Innovation"]},
    "sports":      {"trending_topics":["Match Highlights","Sports Reels","Cricket Fever","Football Goals","Athlete Life"],
                    "viral_hashtags":["#Sports","#Cricket","#Football","#Athletes","#SportsMotivation"]},
    "entertainment":{"trending_topics":["Movie Reviews","Web Series","Meme Content","Celebrity News","Comedy Reels"],
                    "viral_hashtags":["#Entertainment","#Movies","#Comedy","#Memes","#Trending"]},
    "romantic":    {"trending_topics":["Couple Goals","Love Story","Relationship Advice","Date Ideas","Cute Couples"],
                    "viral_hashtags":["#Love","#Couple","#CoupleGoals","#Romance","#RelationshipGoals"]},
    "sad":         {"trending_topics":["Emotional Content","Mental Health","Healing Journey","Overthinking","Self Love"],
                    "viral_hashtags":["#Feelings","#MentalHealth","#Healing","#Relatable","#Emotions"]},
    "general":     {"trending_topics":["Viral Reels","Trending Audio","Emotional Content","Motivation","Life Tips"],
                    "viral_hashtags":["#Trending","#Viral","#ExplorePage","#FYP","#ReelsIndia"]},
}
 
KEYWORD_CATEGORY_MAP = {
    "fashion":"fashion","style":"fashion","ootd":"fashion","outfit":"fashion","clothing":"fashion",
    "motivation":"motivation","motivational":"motivation","inspire":"motivation","mindset":"motivation","success":"motivation","hustle":"motivation",
    "travel":"travel","trip":"travel","vacation":"travel","tour":"travel","explore":"travel",
    "fitness":"fitness","gym":"fitness","workout":"fitness","exercise":"fitness","training":"fitness",
    "food":"food","recipe":"food","cooking":"food","eat":"food","restaurant":"food",
    "tech":"technology","technology":"technology","ai":"technology","gadget":"technology","coding":"technology",
    "sports":"sports","cricket":"sports","football":"sports","ipl":"sports","basketball":"sports",
    "movie":"entertainment","comedy":"entertainment","meme":"entertainment","actor":"entertainment","cinema":"entertainment",
    "love":"romantic","romantic":"romantic","couple":"romantic","relationship":"romantic",
    "sad":"sad","heartbreak":"sad","miss":"sad","alone":"sad","pain":"sad",
    "pet":"pet","dog":"pet","cat":"pet","animal":"pet",
}
 
 
# -----------------------------------
# 1. GOOGLE TRENDS (real-time)
# -----------------------------------
 
def fetch_google_trends(keyword, region="IN"):
    try:
        from pytrends.request import TrendReq
        time.sleep(2)
        pytrends = TrendReq(hl='en-US', tz=330, timeout=(10, 25))
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo=region)
        related = pytrends.related_queries()
        topics  = []
        if keyword in related:
            if related[keyword]["top"] is not None:
                topics = related[keyword]["top"]["query"].head(5).tolist()
            if not topics and related[keyword]["rising"] is not None:
                topics = related[keyword]["rising"]["query"].head(5).tolist()
        print(f"GOOGLE TRENDS: {len(topics)} topics for '{keyword}'")
        return {"source": "Google Trends (live)", "topics": topics}
    except Exception as e:
        print(f"GOOGLE TRENDS ERROR: {e}")
        return {"source": "Google Trends (failed)", "topics": []}
 
 
# -----------------------------------
# 2. YOUTUBE TRENDS (real-time)
# -----------------------------------
 
def fetch_youtube_trends(keyword, region="IN"):
    if not YOUTUBE_API_KEY:
        return {"source": "YouTube (no API key)", "topics": [], "videos": []}
    try:
        # Fetch trending videos for keyword
        url    = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part":             "snippet",
            "q":                f"{keyword} reels shorts trending 2025",
            "type":             "video",
            "order":            "viewCount",
            "maxResults":       5,
            "regionCode":       region,
            "relevanceLanguage":"en",
            "key":              YOUTUBE_API_KEY,
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
 
        if "error" in data:
            print(f"YOUTUBE TRENDS ERROR: {data['error']['message']}")
            return {"source": "YouTube (error)", "topics": [], "videos": []}
 
        videos = []
        topics = []
        for item in data.get("items", []):
            title   = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            vid_id  = item["id"]["videoId"]
            videos.append({
                "title":   title[:60],
                "channel": channel,
                "url":     f"https://youtube.com/watch?v={vid_id}"
            })
            # extract clean topic from title
            clean = title.split("|")[0].split("-")[0].strip()[:40]
            if clean not in topics:
                topics.append(clean)
 
        print(f"YOUTUBE TRENDS: {len(videos)} videos for '{keyword}'")
        return {"source": "YouTube Trending (live)", "topics": topics[:5], "videos": videos}
 
    except Exception as e:
        print(f"YOUTUBE TRENDS FETCH ERROR: {e}")
        return {"source": "YouTube (failed)", "topics": [], "videos": []}
 
 
# -----------------------------------
# 3. INSTAGRAM TRENDS (via hashtag popularity)
# Using public hashtag data workaround
# -----------------------------------
 
def fetch_instagram_trends(keyword, category):
    """
    Instagram has no free official API.
    We use category-based trending hashtag
    intelligence built from real patterns.
    Returns trending hashtag suggestions
    with estimated reach tiers.
    """
    try:
        # Trending Instagram hashtags by category (updated patterns)
        INSTAGRAM_TRENDS = {
            "motivation": {
                "mega":   ["#Motivation", "#Success", "#Mindset"],
                "large":  ["#DailyMotivation", "#GrowthMindset", "#Hustle"],
                "niche":  ["#MorningMotivation", "#SuccessMindset", "#BossLife"],
                "rising": ["#GlowUp", "#LevelUp", "#ElevateYourMind"]
            },
            "fashion": {
                "mega":   ["#Fashion", "#Style", "#OOTD"],
                "large":  ["#FashionReels", "#Outfitcheck", "#FashionBlogger"],
                "niche":  ["#IndianFashion", "#StreetStyle", "#Thrift"],
                "rising": ["#SlowFashion", "#ThriftFlip", "#Y2KFashion"]
            },
            "fitness": {
                "mega":   ["#Fitness", "#Gym", "#Workout"],
                "large":  ["#FitnessMotivation", "#GymLife", "#FitLife"],
                "niche":  ["#HomeWorkout", "#Calisthenics", "#FitnessJourney"],
                "rising": ["#FunctionalFitness", "#75Hard", "#GymReels"]
            },
            "food": {
                "mega":   ["#Food", "#Foodie", "#FoodPhotography"],
                "large":  ["#FoodReels", "#InstaFood", "#FoodBlogger"],
                "niche":  ["#HomeCooking", "#StreetFood", "#RecipeReels"],
                "rising": ["#AirFryerRecipes", "#HighProteinMeals", "#FoodTok"]
            },
            "travel": {
                "mega":   ["#Travel", "#Wanderlust", "#TravelGram"],
                "large":  ["#TravelReels", "#Adventure", "#Explore"],
                "niche":  ["#HiddenGems", "#SoloTravel", "#BudgetTravel"],
                "rising": ["#VanLife", "#DigitalNomad", "#TravelIndia"]
            },
            "sports": {
                "mega":   ["#Cricket", "#Football", "#Sports"],
                "large":  ["#IPL", "#SportsReels", "#Athletes"],
                "niche":  ["#CricketIndia", "#BCCI", "#SportsMotivation"],
                "rising": ["#CricketShorts", "#SportsTok", "#ViralSports"]
            },
            "technology": {
                "mega":   ["#Technology", "#AI", "#Tech"],
                "large":  ["#TechReels", "#Gadgets", "#Innovation"],
                "niche":  ["#AITools", "#CodingLife", "#TechTips"],
                "rising": ["#ChatGPT", "#AIGenerated", "#FutureTech"]
            },
            "romantic": {
                "mega":   ["#Love", "#Couple", "#Romance"],
                "large":  ["#CoupleGoals", "#RelationshipGoals", "#CoupleReels"],
                "niche":  ["#LoveStory", "#Soulmate", "#DateNight"],
                "rising": ["#CoupleContent", "#RelationshipAdvice", "#LoveReels"]
            },
            "general": {
                "mega":   ["#Trending", "#Viral", "#Reels"],
                "large":  ["#ExplorePage", "#FYP", "#ForYou"],
                "niche":  ["#ReelsIndia", "#ViralReels", "#TrendingNow"],
                "rising": ["#ReelItFeelIt", "#ShareReels", "#InstagramReels"]
            }
        }
 
        cat_data = INSTAGRAM_TRENDS.get(category, INSTAGRAM_TRENDS["general"])
 
        all_hashtags = (
            cat_data["mega"][:2] +
            cat_data["large"][:3] +
            cat_data["niche"][:2] +
            cat_data["rising"][:2]
        )
 
        # Add keyword-specific tag
        keyword_tag = f"#{keyword.strip().capitalize()}"
        if keyword_tag not in all_hashtags:
            all_hashtags.insert(0, keyword_tag)
 
        print(f"INSTAGRAM TRENDS: {len(all_hashtags)} hashtags for '{category}'")
        return {
            "source":    "Instagram Trend Intelligence",
            "hashtags":  all_hashtags,
            "mega_tags": cat_data["mega"],
            "niche_tags": cat_data["niche"],
            "rising_tags": cat_data["rising"]
        }
 
    except Exception as e:
        print(f"INSTAGRAM TRENDS ERROR: {e}")
        return {"source": "Instagram (failed)", "hashtags": [], "mega_tags": [], "niche_tags": [], "rising_tags": []}
 
 
# -----------------------------------
# DETECT CATEGORY FROM KEYWORD
# -----------------------------------
 
def _detect_category(keyword):
    kw = keyword.lower().strip()
    for k, cat in KEYWORD_CATEGORY_MAP.items():
        if k in kw:
            return cat
    return "general"
 
 
# -----------------------------------
# GET REGIONAL SONGS
# -----------------------------------
 
def get_regional_songs(category, region="IN", lang_key=""):
    # state-specific first
    if lang_key and lang_key in REGIONAL_SONGS:
        state_songs = REGIONAL_SONGS[lang_key].get(category,
                      REGIONAL_SONGS[lang_key].get("general", []))
        in_songs    = REGIONAL_SONGS.get("IN",{}).get(category,
                      REGIONAL_SONGS["IN"]["general"])
        combined    = list(dict.fromkeys(state_songs + in_songs))
        random.shuffle(combined)
        return combined[:6]
    if region == "IN":
        tn_songs = REGIONAL_SONGS.get("TN", {}).get(category, [])
        in_songs  = REGIONAL_SONGS.get("IN", {}).get(category, REGIONAL_SONGS["IN"]["general"])
        combined = list(dict.fromkeys(in_songs + tn_songs))
        random.shuffle(combined)
        return combined[:6]
    region_db = REGIONAL_SONGS.get(region, REGIONAL_SONGS["IN"])
    songs     = region_db.get(category, region_db.get("general", []))
    random.shuffle(songs)
    return songs[:6]
 
 
# -----------------------------------
# GET REGIONAL HASHTAGS
# -----------------------------------
 
def get_regional_hashtags(category, region="IN"):
    region_db = REGIONAL_HASHTAGS.get(region, REGIONAL_HASHTAGS["IN"])
    tags      = region_db.get(category, region_db.get("general", []))
    return tags[:5]
 
 
# -----------------------------------
# MAIN TREND ANALYZER
# Fetches from Google + YouTube + Instagram
# -----------------------------------
 
def get_realtime_trends(keyword="viral", region="IN", state="", visual_category=""):
 
    # Use visual category directly if provided (most accurate)
    category = visual_category if visual_category else _detect_category(keyword)
 
    # map state code to song db key
    STATE_TO_LANG = {
        "IN-TN":"TN","IN-AP":"TE","IN-TS":"TE","IN-KL":"ML",
        "IN-KA":"KA","IN-MH":"MH","IN-PB":"PB","IN-WB":"WB",
        "IN-GJ":"GJ","IN-BR":"BH",
    }
    lang_key = STATE_TO_LANG.get(state, "") if state else ""
 
    print(f"\nTREND ANALYSIS: keyword='{keyword}', category='{category}', region='{region}', state='{state}', lang='{lang_key}'")
 
    # -----------------------------------
    # FETCH FROM ALL 3 SOURCES
    # -----------------------------------
 
    google_data    = fetch_google_trends(keyword, region)
    youtube_data   = fetch_youtube_trends(keyword, region)
    instagram_data = fetch_instagram_trends(keyword, category)
 
    # -----------------------------------
    # MERGE TRENDING TOPICS
    # Google + YouTube topics combined
    # -----------------------------------
 
    all_topics = []
 
    # Google topics first (most reliable)
    for t in google_data["topics"]:
        if t not in all_topics:
            all_topics.append(t)
 
    # YouTube topics next
    for t in youtube_data["topics"]:
        if t not in all_topics:
            all_topics.append(t)
 
    # Fallback if both failed
    if not all_topics:
        fallback = TREND_DATABASE.get(category, TREND_DATABASE["general"])
        all_topics = fallback["trending_topics"].copy()
        random.shuffle(all_topics)
        print("TREND: Using fallback database")
 
    # -----------------------------------
    # BUILD HASHTAGS
    # Instagram + Region + Trend + Keyword
    # -----------------------------------
 
    hashtags = []
 
    # 1. keyword tag
    kw_tag = f"#{keyword.strip().capitalize()}"
    hashtags.append(kw_tag)
 
    # 2. Instagram trending tags
    for tag in instagram_data.get("hashtags", [])[:6]:
        if tag not in hashtags:
            hashtags.append(tag)
 
    # 3. Regional hashtags
    for tag in get_regional_hashtags(category, region):
        if tag not in hashtags:
            hashtags.append(tag)
 
    # 4. Core viral tags
    for tag in ["#Trending", "#Viral", "#FYP", "#ExplorePage", "#Reels"]:
        if tag not in hashtags:
            hashtags.append(tag)
 
    # -----------------------------------
    # REGIONAL SONGS
    # -----------------------------------
 
    regional_songs = get_regional_songs(category, region, lang_key)
 
    # -----------------------------------
    # TREND STRENGTH
    # -----------------------------------
 
    google_live = len(google_data["topics"]) > 0
    youtube_live = len(youtube_data["topics"]) > 0
 
    if google_live and youtube_live:
        trend_strength = "Very High"
    elif google_live or youtube_live:
        trend_strength = "High"
    elif len(all_topics) >= 3:
        trend_strength = "Medium"
    else:
        trend_strength = "Low"
 
    # -----------------------------------
    # DATA SOURCES SUMMARY
    # -----------------------------------
 
    sources_used = []
    if google_live:    sources_used.append("Google Trends")
    if youtube_live:   sources_used.append("YouTube Trending")
    sources_used.append("Instagram Intelligence")
    if not (google_live or youtube_live): sources_used.append("Fallback DB")
 
    print(f"TREND RESULT: {len(all_topics)} topics, {len(hashtags)} hashtags, strength={trend_strength}")
    print(f"SOURCES: {', '.join(sources_used)}")
 
    return {
        "main_keyword":       keyword,
        "category":           category,
        "trending_topics":    all_topics[:5],
        "trend_strength":     trend_strength,
        "hashtags":           hashtags[:12],
 
        # Instagram specific
        "instagram_hashtags": instagram_data.get("hashtags", [])[:8],
        "instagram_mega_tags":  instagram_data.get("mega_tags", []),
        "instagram_niche_tags": instagram_data.get("niche_tags", []),
        "instagram_rising_tags":instagram_data.get("rising_tags", []),
 
        # YouTube specific
        "youtube_trending_videos": youtube_data.get("videos", [])[:3],
 
        # Regional songs suggestion
        "regional_songs":     regional_songs,
        "region_code":        region,
 
        # Meta
        "sources_used":       sources_used,
        "google_live":        google_live,
        "youtube_live":       youtube_live,
    }