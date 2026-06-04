import os
import requests
import random
from dotenv import load_dotenv
 
load_dotenv()
 
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
 
# -----------------------------------
# FALLBACK SONG DATABASE
# Only used if YouTube API fails
# Organized by content type + region
# -----------------------------------
 
FALLBACK_SONGS = {
 
    "IN": {  # India
        "fashion":     ["Hukum", "Arabic Kuthu", "Manike", "Bijlee Bijlee", "Jhoome Jo Pathaan"],
        "fitness":     ["Believer", "Hall of Fame", "Unstoppable", "Vaathi Coming", "Besharam Rang"],
        "motivation":  ["Kar Har Maidaan Fateh", "Zinda", "Sultan", "Mary Kom Theme", "Dangal"],
        "food":        ["Enjoy Enjaami", "Shape of You", "Swag Se Swagat", "Param Sundari"],
        "travel":      ["Ilahi", "Safarnama", "Tum Ho", "Zindagi Na Milegi Dobara Theme"],
        "romantic":    ["Kesariya", "Tum Hi Ho", "Raataan Lambiyan", "Ik Vaari Aa", "Munbe Vaa"],
        "sad":         ["Channa Mereya", "Ae Dil Hai Mushkil", "Tujhe Kitna Chahne Lage", "Life of Ram"],
        "sports":      ["Naatu Naatu", "Dangal Theme", "Sultan Theme", "Jag Ghoomeya"],
        "comedy":      ["Gallan Goodiyaan", "Saturday Saturday", "London Thumakda"],
        "technology":  ["Zinda", "Believer", "The Spectre", "Centuries"],
        "pet":         ["Cute", "Happy", "Perfect", "Can't Stop the Feeling"],
        "general":     ["Naatu Naatu", "Jawan Theme", "Vaathi Coming", "Hukum", "Kesariya"],
    },
 
    "US": {  # USA
        "fashion":     ["Industry Baby", "Bad Guy", "Levitating", "As It Was", "Flowers"],
        "fitness":     ["Eye of the Tiger", "Stronger", "Till I Collapse", "Power", "Lose Yourself"],
        "motivation":  ["Hall of Fame", "Roar", "Fight Song", "Titanium", "Unstoppable"],
        "food":        ["Happy", "Good as Hell", "Can't Stop the Feeling", "Shake It Off"],
        "travel":      ["Mr. Brightside", "Take Me Home Country Roads", "Life is a Highway"],
        "romantic":    ["Perfect", "All of Me", "A Thousand Years", "Thinking Out Loud"],
        "sad":         ["Someone Like You", "Fix You", "The Night We Met", "Skinny Love"],
        "sports":      ["Eye of the Tiger", "We Will Rock You", "Jump Around", "Lose Yourself"],
        "comedy":      ["Happy", "Can't Stop the Feeling", "Uptown Funk", "24K Magic"],
        "technology":  ["Centuries", "The Spectre", "Radioactive", "Warriors"],
        "general":     ["As It Was", "Flowers", "Levitating", "Industry Baby", "Stay"],
    }
}
 
# content type → music category mapping
CONTENT_TO_MUSIC = {
    "Human / Lifestyle Content":        "general",
    "Professional / Business Content":  "motivation",
    "Fitness Content":                  "fitness",
    "Food & Lifestyle Content":         "food",
    "Food Content":                     "food",
    "Sports Content":                   "sports",
    "Technology Content":               "technology",
    "Music / Entertainment Content":    "general",
    "Travel Content":                   "travel",
    "Pet / Animal Content":             "pet",
    "Automobile Content":               "motivation",
    "General Viral Content":            "general",
}
 
# keyword → music category
KEYWORD_TO_MUSIC = {
    "motivation": "motivation", "motivational": "motivation", "inspire": "motivation",
    "fitness":    "fitness",    "gym":          "fitness",    "workout": "fitness",
    "food":       "food",       "recipe":       "food",       "cooking": "food",
    "travel":     "travel",     "trip":         "travel",     "vacation":"travel",
    "fashion":    "fashion",    "style":        "fashion",    "ootd":    "fashion",
    "sad":        "sad",        "heartbreak":   "sad",        "miss":    "sad",
    "love":       "romantic",   "romantic":     "romantic",   "couple":  "romantic",
    "sports":     "sports",     "cricket":      "sports",     "football":"sports",
    "tech":       "technology", "ai":           "technology", "coding":  "technology",
    "comedy":     "comedy",     "funny":        "comedy",     "meme":    "comedy",
    "pet":        "pet",        "dog":          "pet",        "cat":     "pet",
}
 
# reel style per music category
REEL_STYLES = {
    "fashion":    "Slow-motion + Outfit Reveal Cuts",
    "fitness":    "Fast Cuts + Transformation Reveal",
    "motivation": "Text Overlay + Cinematic Cuts",
    "food":       "Close-up Shots + Slow Pour Cuts",
    "travel":     "Time-lapse + Scenic Wide Shots",
    "romantic":   "Soft Transitions + Candid Shots",
    "sad":        "Slow Fade + Emotional Expressions",
    "sports":     "Fast Action Cuts + Slow Motion Replay",
    "comedy":     "Jump Cuts + Reaction Shots",
    "technology": "Screen Recording + Fast Cuts",
    "pet":        "Candid + Slow Motion Cute Moments",
    "general":    "Fast Cuts + Trending Audio",
}
 
 
# -----------------------------------
# YOUTUBE REAL-TIME TRENDING SONGS
# -----------------------------------
 
def fetch_youtube_trending_music(content_type, region="IN"):
    """
    Fetch real trending music from YouTube Data API v3
    Searches for trending audio matching the content type
    """
 
    if not YOUTUBE_API_KEY:
        print("MUSIC: No YouTube API key — using fallback database")
        return []
 
    try:
 
        # map content type to search query
        music_category = CONTENT_TO_MUSIC.get(content_type, "general")
 
        search_queries = {
            "fashion":    f"trending fashion reels song {region} 2025",
            "fitness":    f"trending gym workout music {region} 2025",
            "motivation": f"trending motivation background music 2025",
            "food":       f"trending food reels music 2025",
            "travel":     f"trending travel reels background music 2025",
            "romantic":   f"trending romantic songs {region} 2025",
            "sad":        f"trending sad songs {region} 2025",
            "sports":     f"trending sports background music 2025",
            "comedy":     f"trending funny reels music 2025",
            "technology": f"trending tech background music 2025",
            "general":    f"trending reels songs {region} 2025",
            "pet":        f"trending cute pet video music 2025",
        }
 
        query = search_queries.get(music_category, f"trending songs {region} 2025")
 
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part":          "snippet",
            "q":             query,
            "type":          "video",
            "videoCategoryId": "10",   # Music category
            "order":         "viewCount",
            "maxResults":    8,
            "regionCode":    region,
            "relevanceLanguage": "en",
            "key":           YOUTUBE_API_KEY
        }
 
        response = requests.get(url, params=params, timeout=10)
        data     = response.json()
 
        if "error" in data:
            print(f"YOUTUBE API ERROR: {data['error']['message']}")
            return []
 
        songs = []
        for item in data.get("items", []):
            title     = item["snippet"]["title"]
            channel   = item["snippet"]["channelTitle"]
            video_id  = item["id"]["videoId"]
 
            # clean title — remove common noise
            clean_title = (
                title
                .replace("(Official Video)", "")
                .replace("(Official Music Video)", "")
                .replace("(Lyric Video)", "")
                .replace("(Audio)", "")
                .replace("| Official Video", "")
                .replace("ft.", "feat.")
                .strip()
            )
 
            songs.append({
                "title":    clean_title,
                "channel":  channel,
                "url":      f"https://youtube.com/watch?v={video_id}",
                "source":   "YouTube Trending"
            })
 
        print(f"MUSIC: Fetched {len(songs)} real trending songs from YouTube")
        return songs
 
    except Exception as e:
        print(f"YOUTUBE MUSIC FETCH ERROR: {e}")
        return []
 
 
# -----------------------------------
# DETECT MUSIC CATEGORY FROM INPUT
# -----------------------------------
 
def detect_music_category(visual_data, caption_data):
 
    # check caption keywords first
    keywords = caption_data.get("keywords", [])
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in KEYWORD_TO_MUSIC:
            return KEYWORD_TO_MUSIC[kw_lower]
 
    # check original caption text
    caption_text = caption_data.get("original_caption", "").lower()
    for kw, cat in KEYWORD_TO_MUSIC.items():
        if kw in caption_text:
            return cat
 
    # check content type from visual
    content_type = visual_data.get("content_type", "")
    return CONTENT_TO_MUSIC.get(content_type, "general")
 
 
# -----------------------------------
# MAIN MUSIC ANALYZER
# -----------------------------------
 
def recommend_music(visual_data, caption_data, trend_data, region="IN"):
 
    content_type   = visual_data.get("content_type", "General Viral Content")
    # Use primary_category directly from visual analysis
    primary_category = visual_data.get("primary_category", "")
    music_category = primary_category if primary_category else detect_music_category(visual_data, caption_data)
 
    print(f"MUSIC: visual_category={primary_category}, music_category={music_category}, region={region}")
 
    # -----------------------------------
    # TRY YOUTUBE API FIRST (real-time)
    # -----------------------------------
 
    youtube_songs = fetch_youtube_trending_music(content_type, region)
 
    if youtube_songs:
 
        # return rich response with YouTube data
        song_titles = [s["title"] for s in youtube_songs[:5]]
 
        return {
            "recommended_songs":    song_titles,
            "song_details":         youtube_songs[:5],
            "music_category":       music_category,
            "music_strategy": {
                "best_reel_style":          REEL_STYLES.get(music_category, "Fast Cuts + Trending Audio"),
                "recommended_platform":     _best_platform_for_music(content_type),
                "viral_audio_probability":  _viral_probability(music_category),
            },
            "source": "YouTube Trending (live)"
        }
 
    # -----------------------------------
    # FALLBACK — local database
    # -----------------------------------
 
    print("MUSIC: Using fallback song database")
 
    region_key  = "IN" if region == "IN" else "US"
    region_db   = FALLBACK_SONGS.get(region_key, FALLBACK_SONGS["IN"])
    songs       = region_db.get(music_category, region_db["general"])
 
    # deduplicate and shuffle for variety
    unique_songs = list(dict.fromkeys(songs))
    random.shuffle(unique_songs)
 
    return {
        "recommended_songs":   unique_songs[:5],
        "song_details":        [],
        "music_category":      music_category,
        "music_strategy": {
            "best_reel_style":         REEL_STYLES.get(music_category, "Fast Cuts + Trending Audio"),
            "recommended_platform":    _best_platform_for_music(content_type),
            "viral_audio_probability": _viral_probability(music_category),
        },
        "source": "Fallback database"
    }
 
 
# -----------------------------------
# HELPERS
# -----------------------------------
 
def _best_platform_for_music(content_type):
    youtube_content = ["Sports Content", "Technology Content", "Travel Content", "Professional / Business Content"]
    return "YouTube Shorts" if content_type in youtube_content else "Instagram Reels"
 
 
def _viral_probability(music_category):
    high   = ["fashion", "fitness", "motivation", "general"]
    medium = ["food", "travel", "sports", "comedy"]
    return "High" if music_category in high else "Medium" if music_category in medium else "Low"