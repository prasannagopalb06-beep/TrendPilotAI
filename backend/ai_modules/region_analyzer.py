# -----------------------------------
# REGION ANALYZER
# -----------------------------------
 
REGION_DATABASE = {
    "IN": {
        "region_name":      "India",
        "languages":        ["Hindi", "English", "Tamil", "Telugu", "Bengali", "Marathi"],
        "best_upload_time": "7 PM - 10 PM IST",
        "best_days":        ["Tuesday", "Wednesday", "Friday", "Saturday"],
        "top_categories":   ["cinema", "motivation", "fitness", "cricket", "food", "fashion", "memes", "devotional"],
        "audience_behavior":"Highly emotional, trend-driven, responds to relatable + cinematic content",
        "viral_factor":     85,
        "avg_watch_time":   "8-12 seconds",
        "platform_priority":["Instagram Reels", "YouTube Shorts", "Facebook Reels"],
    },
    "US": {
        "region_name":      "United States",
        "languages":        ["English", "Spanish"],
        "best_upload_time": "6 PM - 9 PM EST",
        "best_days":        ["Tuesday", "Thursday", "Friday"],
        "top_categories":   ["lifestyle", "fitness", "fashion", "tech", "comedy", "food", "politics"],
        "audience_behavior":"Fast-scrolling, values authenticity, responds to humor and storytelling",
        "viral_factor":     82,
        "avg_watch_time":   "6-10 seconds",
        "platform_priority":["TikTok", "Instagram Reels", "YouTube Shorts"],
    },
    "GB": {
        "region_name":      "United Kingdom",
        "languages":        ["English"],
        "best_upload_time": "7 PM - 10 PM GMT",
        "best_days":        ["Wednesday", "Thursday", "Saturday"],
        "top_categories":   ["football", "fashion", "comedy", "food", "travel", "music"],
        "audience_behavior":"Responds well to dry humor, storytelling, and lifestyle content",
        "viral_factor":     75,
        "avg_watch_time":   "7-11 seconds",
        "platform_priority":["TikTok", "Instagram Reels", "YouTube Shorts"],
    },
    "AU": {
        "region_name":      "Australia",
        "languages":        ["English"],
        "best_upload_time": "6 PM - 9 PM AEST",
        "best_days":        ["Thursday", "Friday", "Saturday"],
        "top_categories":   ["travel", "fitness", "food", "comedy", "lifestyle", "nature"],
        "audience_behavior":"Outdoor and adventure-loving, responds to nature and lifestyle content",
        "viral_factor":     72,
        "avg_watch_time":   "7-10 seconds",
        "platform_priority":["TikTok", "Instagram Reels", "YouTube Shorts"],
    },
    "JP": {
        "region_name":      "Japan",
        "languages":        ["Japanese", "English"],
        "best_upload_time": "8 PM - 11 PM JST",
        "best_days":        ["Friday", "Saturday", "Sunday"],
        "top_categories":   ["anime", "gaming", "food", "travel", "tech", "kawaii"],
        "audience_behavior":"Highly visual, values quality and aesthetics, niche communities",
        "viral_factor":     70,
        "avg_watch_time":   "10-15 seconds",
        "platform_priority":["TikTok", "Instagram Reels", "YouTube Shorts"],
    },
}
 
 
def analyze_region(region, visual_data, caption_data, trend_data):
 
    region_info = REGION_DATABASE.get(region, REGION_DATABASE["IN"])
 
    keywords     = caption_data.get("keywords", [])
    emotion      = caption_data.get("emotion", "general")
    content_type = visual_data.get("content_type", "general").lower()
 
    # -----------------------------------
    # CATEGORY MATCH
    # Check if user content matches
    # what's trending in their region
    # -----------------------------------
 
    top_cats = region_info["top_categories"]
    matched  = []
 
    for kw in keywords:
        if kw.lower() in top_cats:
            matched.append(kw)
 
    for cat in top_cats:
        if cat in content_type.lower():
            if cat not in matched:
                matched.append(cat)
 
    if emotion != "general" and emotion in top_cats:
        matched.append(emotion)
 
    # -----------------------------------
    # REGIONAL VIRAL SCORE
    # -----------------------------------
 
    viral_factor = region_info["viral_factor"]
 
    if len(matched) >= 2:     viral_factor += 10
    elif len(matched) == 1:   viral_factor += 5
    if emotion in ["motivational", "happy", "romantic"]: viral_factor += 5
 
    viral_factor = min(viral_factor, 100)
 
    # -----------------------------------
    # AUDIENCE MATCH SCORE
    # -----------------------------------
 
    audience_match = 40  # base
    audience_match += len(matched) * 15
    audience_match += (5 if emotion != "general" else 0)
    audience_match += (10 if viral_factor >= 85 else 0)
    audience_match = min(int(audience_match), 100)
 
    # -----------------------------------
    # CONTENT RECOMMENDATION
    # -----------------------------------
 
    if matched:
        recommendation = f"Your content matches {', '.join(matched)} — highly relevant for {region_info['region_name']} audience"
    else:
        recommendation = f"Consider adding {region_info['top_categories'][0]} or {region_info['top_categories'][1]} elements for better regional resonance"
 
    return {
        "region":               region_info["region_name"],
        "languages":            region_info["languages"],
        "best_upload_time":     region_info["best_upload_time"],
        "best_days":            region_info["best_days"],
        "top_categories":       region_info["top_categories"],
        "audience_behavior":    region_info["audience_behavior"],
        "avg_watch_time":       region_info["avg_watch_time"],
        "platform_priority":    region_info["platform_priority"],
        "matched_categories":   matched,
        "regional_viral_score": viral_factor,
        "audience_match_score": audience_match,
        "recommendation":       recommendation,
    }