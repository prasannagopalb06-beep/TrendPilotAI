# -----------------------------------
# ENGAGEMENT PREDICTOR
# Uses all module data properly
# -----------------------------------
 
def predict_engagement(visual_data, caption_data, trend_data, music_data):
 
    # -----------------------------------
    # COLLECT ALL SIGNALS
    # -----------------------------------
 
    visual_score    = float(visual_data.get("visual_score", 50))
    object_count    = int(visual_data.get("object_count", 0))
    viral_potential = visual_data.get("viral_potential", "Low")
    thumbnail_q     = visual_data.get("thumbnail_quality", "Average")
    has_person      = "person" in visual_data.get("detected_objects", [])
 
    word_count      = int(caption_data.get("word_count", 0))
    has_hashtags    = bool(caption_data.get("has_hashtags", False))
    has_emojis      = bool(caption_data.get("has_emojis", False))
    emotion         = caption_data.get("emotion", "general")
    caption_quality = caption_data.get("caption_quality", "Average")
 
    trend_strength  = trend_data.get("trend_strength", "Low")
    trend_topics    = len(trend_data.get("trending_topics", []))
    trend_source    = trend_data.get("source", "")
 
    music_category  = music_data.get("music_category", "general")
    viral_audio     = music_data.get("music_strategy", {}).get("viral_audio_probability", "Low")
 
    # -----------------------------------
    # BASE SCORE
    # -----------------------------------
 
    score = 0
 
    # VISUAL (40% weight)
    score += visual_score * 0.4
 
    # CAPTION (20% weight)
    caption_score = 0
    if word_count >= 10:     caption_score += 30
    elif word_count >= 5:    caption_score += 20
    elif word_count >= 2:    caption_score += 10
    if has_hashtags:         caption_score += 20
    if has_emojis:           caption_score += 15
    if caption_quality == "Excellent": caption_score += 20
    elif caption_quality == "Good":    caption_score += 10
    caption_score = min(caption_score, 100)
    score += caption_score * 0.2
 
    # TREND (25% weight)
    trend_score = 0
    if trend_strength == "High":   trend_score = 90
    elif trend_strength == "Medium": trend_score = 65
    else:                            trend_score = 35
    if trend_source == "Google Trends (live)": trend_score += 10
    if trend_topics >= 4:          trend_score += 10
    trend_score = min(trend_score, 100)
    score += trend_score * 0.25
 
    # MUSIC BOOST (10% weight)
    music_score = 0
    if viral_audio == "High":   music_score = 90
    elif viral_audio == "Medium": music_score = 65
    else:                         music_score = 40
    score += music_score * 0.10
 
    # BONUS FACTORS (5% weight)
    bonus = 0
    if has_person:           bonus += 15
    if object_count >= 3:    bonus += 10
    if thumbnail_q == "Excellent": bonus += 15
    elif thumbnail_q == "Good":    bonus += 8
    if emotion in ["motivational","happy","romantic"]: bonus += 10
    bonus = min(bonus, 100)
    score += bonus * 0.05
 
    score = min(round(score, 1), 100)
 
    # -----------------------------------
    # ENGAGEMENT LEVEL
    # -----------------------------------
 
    if score >= 80:
        level = "High"
        reach = "Viral Reach (100K+ views potential)"
    elif score >= 65:
        level = "Medium-High"
        reach = "High Reach (10K-100K views)"
    elif score >= 50:
        level = "Medium"
        reach = "Moderate Reach (1K-10K views)"
    elif score >= 35:
        level = "Low-Medium"
        reach = "Limited Reach (100-1K views)"
    else:
        level = "Low"
        reach = "Low Reach (under 100 views)"
 
    # -----------------------------------
    # BEST ENGAGEMENT FACTOR
    # -----------------------------------
 
    factors = {
        "Visual Quality":   visual_score,
        "Trending Topic":   trend_score,
        "Caption Quality":  caption_score,
        "Music Relevance":  music_score,
    }
    best_factor = max(factors, key=factors.get)
 
    # -----------------------------------
    # IMPROVEMENT TIPS
    # -----------------------------------
 
    tips = []
    if not has_hashtags:   tips.append("Add hashtags to your caption")
    if not has_emojis:     tips.append("Add emojis for emotional connection")
    if word_count < 5:     tips.append("Write a longer, more descriptive caption")
    if thumbnail_q in ["Average","Poor — low resolution"]:
        tips.append("Improve image quality to at least 720p")
    if trend_strength == "Low":
        tips.append("Use trending keywords related to your content")
    if viral_audio == "Low":
        tips.append("Use trending audio for higher reach")
 
    return {
        "engagement_score":       score,
        "engagement_probability": level,
        "estimated_reach":        reach,
        "best_engagement_factor": best_factor,
        "improvement_tips":       tips[:3],
        "score_breakdown": {
            "visual":   round(visual_score * 0.4, 1),
            "caption":  round(caption_score * 0.2, 1),
            "trend":    round(trend_score * 0.25, 1),
            "music":    round(music_score * 0.10, 1),
            "bonus":    round(bonus * 0.05, 1),
        }
    }