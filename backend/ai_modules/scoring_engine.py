def calculate_virality_score(
    visual_data,
    caption_data,
    trend_data,
    content_data
):

    score = 0

    reasons = []

    # -----------------------------------
    # VISUAL QUALITY
    # -----------------------------------

    aesthetic_score = visual_data.get(
        "aesthetic_score",
        5
    )

    if aesthetic_score >= 8:
        score += 25
        reasons.append(
            "High aesthetic quality"
        )

    elif aesthetic_score >= 6:
        score += 15
        reasons.append(
            "Good visual appearance"
        )

    # -----------------------------------
    # EMOTIONAL CONTENT
    # -----------------------------------

    emotion = caption_data.get(
        "emotion",
        ""
    ).lower()

    if emotion in [
        "happy",
        "motivational",
        "emotional",
        "excited"
    ]:
        score += 15
        reasons.append(
            "Strong emotional engagement"
        )

    # -----------------------------------
    # TREND MATCHING
    # -----------------------------------

    trend_score = trend_data.get(
        "trend_score",
        5
    )

    score += trend_score * 2

    if trend_score >= 7:
        reasons.append(
            "Matches current trends"
        )

    # -----------------------------------
    # INSTAGRAM STYLE BOOST
    # -----------------------------------

    labels = content_data.get(
        "content_labels",
        []
    )

    if "instagram_style" in labels:
        score += 20
        reasons.append(
            "Instagram aesthetic detected"
        )

    if "aesthetic" in labels:
        score += 10

    if "fashion" in labels:
        score += 8

    if "travel" in labels:
        score += 8

    if "fitness" in labels:
        score += 7

    # -----------------------------------
    # CAPTION QUALITY
    # -----------------------------------

    engagement = caption_data.get(
        "engagement_score",
        5
    )

    score += engagement * 2

    # -----------------------------------
    # LIMIT SCORE
    # -----------------------------------

    if score > 100:
        score = 100

    # -----------------------------------
    # FINAL OUTPUT
    # -----------------------------------

    if score >= 80:
        viral_level = "Very High"

    elif score >= 60:
        viral_level = "High"

    elif score >= 40:
        viral_level = "Medium"

    else:
        viral_level = "Low"

    return {
        "virality_score": score,
        "viral_level": viral_level,
        "score_reasons": reasons
    }