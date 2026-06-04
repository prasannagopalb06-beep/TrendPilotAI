# -----------------------------------
# PLATFORM DATABASE
# -----------------------------------
 
PLATFORM_DATABASE = {
 
    "Instagram Reels": {
        "best_for":           ["fashion", "fitness", "food", "travel", "lifestyle", "motivation", "beauty"],
        "content_style":      "Short engaging reels with trending audio",
        "posting_frequency":  "1-2 reels daily",
        "best_duration":      "15-30 seconds",
        "best_time":          "7 PM - 10 PM",
        "algorithm_tip":      "Use Reels + Stories combo for maximum reach"
    },
 
    "YouTube Shorts": {
        "best_for":           ["education", "motivation", "travel", "cinematic", "tech", "sports", "business"],
        "content_style":      "Hook-based shorts with strong opening 3 seconds",
        "posting_frequency":  "1 short daily",
        "best_duration":      "20-45 seconds",
        "best_time":          "6 PM - 9 PM",
        "algorithm_tip":      "Add chapters and pinned comments to boost watch time"
    },
 
    "TikTok": {
        "best_for":           ["funny", "dance", "viral", "trendy", "comedy", "entertainment"],
        "content_style":      "Fast viral content with trending sounds",
        "posting_frequency":  "2-3 posts daily",
        "best_duration":      "10-20 seconds",
        "best_time":          "6 PM - 9 PM",
        "algorithm_tip":      "Use duets and stitches to ride trending content"
    },
 
    "Facebook Reels": {
        "best_for":           ["family", "community", "news", "local", "business", "general"],
        "content_style":      "Relatable and community-driven content",
        "posting_frequency":  "1 reel daily",
        "best_duration":      "20-40 seconds",
        "best_time":          "8 PM - 11 PM",
        "algorithm_tip":      "Share to groups for extra organic reach"
    }
}
 
# -----------------------------------
# REGION → PLATFORM RESTRICTIONS
# TikTok is banned in India
# -----------------------------------
 
REGION_PLATFORM_PRIORITY = {
    "IN": ["Instagram Reels", "YouTube Shorts", "Facebook Reels"],
    "US": ["TikTok", "Instagram Reels", "YouTube Shorts"],
    "GB": ["TikTok", "Instagram Reels", "YouTube Shorts"],
    "AU": ["TikTok", "Instagram Reels", "YouTube Shorts"],
    "PK": ["TikTok", "Instagram Reels", "YouTube Shorts"],
}
 
# content type → best platform mapping
CONTENT_PLATFORM_MAP = {
    "Human / Lifestyle Content":        "Instagram Reels",
    "Professional / Business Content":  "YouTube Shorts",
    "Fitness Content":                  "Instagram Reels",
    "Food & Lifestyle Content":         "Instagram Reels",
    "Food Content":                     "Instagram Reels",
    "Sports Content":                   "YouTube Shorts",
    "Technology Content":               "YouTube Shorts",
    "Music / Entertainment Content":    "Instagram Reels",
    "Travel Content":                   "YouTube Shorts",
    "Pet / Animal Content":             "Instagram Reels",
    "Automobile Content":               "YouTube Shorts",
    "General Viral Content":            "Instagram Reels",
}
 
# region → best upload time
REGION_TIMING = {
    "IN": "7 PM - 10 PM IST",
    "US": "6 PM - 9 PM EST",
    "GB": "7 PM - 10 PM GMT",
    "AU": "6 PM - 9 PM AEST",
}
 
# strategy tips per platform
STRATEGY_TIPS = {
    "Instagram Reels": [
        "Hook viewers in the first 2 seconds",
        "Use trending audio from Reels audio library",
        "Add text overlays and subtitles",
        "Post Reels + Story for 2x reach",
        "Reply to every comment in the first hour",
        "Use 10-15 mixed hashtags (viral + niche)",
        "Keep video quality at minimum 1080p",
    ],
    "YouTube Shorts": [
        "Start with a strong question or hook",
        "Add chapters even for short videos",
        "Use keyword-rich titles and descriptions",
        "Pin a comment to drive engagement",
        "Upload consistently at the same time daily",
        "Use trending topics in your title",
        "End with a clear call-to-action",
    ],
    "TikTok": [
        "Use trending sounds from TikTok discover page",
        "Duet or stitch viral content in your niche",
        "Post 2-3 times daily for algorithm boost",
        "Use 3-5 niche hashtags only",
        "Keep videos under 15 seconds for max loop",
        "Add captions — 80% watch without sound",
        "Go live after posting for extra push",
    ],
    "Facebook Reels": [
        "Share reels to relevant Facebook groups",
        "Tag location for local audience boost",
        "Post at peak family hours (8-11 PM)",
        "Use relatable and emotional content",
        "Add a strong CTA in the caption",
        "Cross-post from Instagram Reels",
        "Respond to comments within 30 minutes",
    ],
}
 
 
# -----------------------------------
# DETECT BEST PLATFORM
# Region-aware — no TikTok for India
# -----------------------------------
 
def detect_best_platform(visual_data, trend_data, region="IN"):
 
    content_type = visual_data.get("content_type", "General Viral Content")
 
    # get ideal platform from content type
    ideal_platform = CONTENT_PLATFORM_MAP.get(
        content_type, "Instagram Reels"
    )
 
    # get allowed platforms for this region
    allowed = REGION_PLATFORM_PRIORITY.get(region, REGION_PLATFORM_PRIORITY["IN"])
 
    # if ideal platform is allowed in this region, use it
    if ideal_platform in allowed:
        return ideal_platform
 
    # otherwise use first allowed platform for this region
    return allowed[0]
 
 
# -----------------------------------
# MAIN PLATFORM STRATEGY
# -----------------------------------
 
def generate_platform_strategy(
 
    visual_data,
    caption_data,
    trend_data,
    engagement_data,
    music_data,
    region="IN"        # ← added region param
):
 
    # -----------------------------------
    # DETECT PLATFORM
    # -----------------------------------
 
    platform      = detect_best_platform(visual_data, trend_data, region)
    platform_info = PLATFORM_DATABASE[platform]
 
    # -----------------------------------
    # VIRAL LEVEL
    # -----------------------------------
 
    engagement_score = engagement_data.get("engagement_score", 60)
    visual_score     = visual_data.get("visual_score", 50)
    combined_score   = (engagement_score + visual_score) / 2
 
    if combined_score >= 80:
        viral_level = "High Viral Potential"
    elif combined_score >= 60:
        viral_level = "Moderate Viral Potential"
    elif combined_score >= 45:
        viral_level = "Low-Medium Viral Potential"
    else:
        viral_level = "Low Viral Potential"
 
    # -----------------------------------
    # BEST TIMING
    # Region-specific timing
    # -----------------------------------
 
    best_time = REGION_TIMING.get(region, platform_info["best_time"])
 
    # -----------------------------------
    # SECONDARY PLATFORMS
    # -----------------------------------
 
    allowed = REGION_PLATFORM_PRIORITY.get(region, ["Instagram Reels", "YouTube Shorts"])
    secondary_platforms = [p for p in allowed if p != platform][:2]
 
    # -----------------------------------
    # OUTPUT
    # -----------------------------------
 
    return {
        "best_platform":               platform,
        "secondary_platforms":         secondary_platforms,
        "viral_level":                 viral_level,
        "best_upload_time":            best_time,
        "recommended_content_style":   platform_info["content_style"],
        "recommended_posting_frequency": platform_info["posting_frequency"],
        "best_video_duration":         platform_info["best_duration"],
        "algorithm_tip":               platform_info["algorithm_tip"],
        "recommended_music":           music_data.get("recommended_songs", [])[:3],
        "strategy_tips":               STRATEGY_TIPS[platform],
        "region":                      region,
    }
 



















