from PIL import Image
from ultralytics import YOLO
import os
 
model = YOLO("yolov8n.pt")
 
# -----------------------------------
# OBJECT → CONTENT CATEGORY MAPPING
# Every detected object maps to a category
# that drives ALL downstream analysis
# -----------------------------------
 
OBJECT_CATEGORY_MAP = {
    # People / Lifestyle
    "person":          "lifestyle",
    "tie":             "business",
    "handbag":         "fashion",
    "backpack":        "travel",
    "suitcase":        "travel",
    "umbrella":        "lifestyle",
 
    # Fashion / Beauty
    "sunglasses":      "fashion",
 
    # Food
    "banana":          "food", "apple":    "food", "sandwich": "food",
    "orange":          "food", "broccoli": "food", "carrot":   "food",
    "hot dog":         "food", "pizza":    "food", "donut":    "food",
    "cake":            "food", "bowl":     "food",
    "bottle":          "food", "cup":      "food", "wine glass":"food",
    "fork":            "food", "knife":    "food", "spoon":    "food",
    "dining table":    "food",
 
    # Sports / Fitness
    "sports ball":     "sports",
    "baseball bat":    "sports", "baseball glove": "sports",
    "skateboard":      "sports", "surfboard":      "sports",
    "tennis racket":   "sports", "frisbee":        "sports",
    "skis":            "sports", "snowboard":      "sports",
    "kite":            "sports",
    "bicycle":         "fitness",
 
    # Technology
    "laptop":          "technology",
    "cell phone":      "technology",
    "keyboard":        "technology",
    "mouse":           "technology",
    "remote":          "technology",
    "tv":              "technology",
    "monitor":         "technology",
 
    # Travel / Outdoors
    "car":             "automobile",
    "motorcycle":      "automobile",
    "bus":             "automobile",
    "truck":           "automobile",
    "airplane":        "travel",
    "boat":            "travel",
    "train":           "travel",
    "bench":           "travel",
    "potted plant":    "nature",
    "bird":            "nature",
    "cat":             "pet",
    "dog":             "pet",
    "horse":           "nature",
    "sheep":           "nature",
    "cow":             "nature",
    "elephant":        "nature",
    "bear":            "nature",
    "zebra":           "nature",
    "giraffe":         "nature",
 
    # Indoor / Lifestyle
    "bed":             "lifestyle",
    "couch":           "lifestyle",
    "chair":           "lifestyle",
    "book":            "education",
    "clock":           "lifestyle",
    "vase":            "lifestyle",
    "scissors":        "lifestyle",
    "toothbrush":      "lifestyle",
 
    # Entertainment
    "microphone":      "entertainment",
    "guitar":          "entertainment",
 
    # Fitness
    "dumbbell":        "fitness",
}
 
# category priority — when multiple detected, pick the most specific
CATEGORY_PRIORITY = [
    "food", "sports", "fitness", "fashion", "technology",
    "travel", "automobile", "pet", "nature", "entertainment",
    "education", "business", "lifestyle"
]
 
# category → content type label
CATEGORY_LABELS = {
    "food":          "Food & Recipe Content",
    "sports":        "Sports Content",
    "fitness":       "Fitness & Gym Content",
    "fashion":       "Fashion & Style Content",
    "technology":    "Technology Content",
    "travel":        "Travel & Adventure Content",
    "automobile":    "Automobile Content",
    "pet":           "Pet & Animal Content",
    "nature":        "Nature & Outdoor Content",
    "entertainment": "Music & Entertainment Content",
    "education":     "Educational Content",
    "business":      "Professional & Business Content",
    "lifestyle":     "Lifestyle Content",
}
 
# object → score weight
OBJECT_SCORES = {
    "person":20,"dog":15,"cat":12,"sports ball":12,"cell phone":10,
    "laptop":10,"car":8,"pizza":10,"cake":10,"food":8,"bicycle":8,
    "motorcycle":8,"airplane":10,"bird":7,"horse":7,"book":5,
    "tie":8,"handbag":8,"microphone":12,"dumbbell":12,"guitar":12,
}
 
# category → mood/feel
CATEGORY_MOOD = {
    "food":          "Warm, Appetizing, Inviting",
    "sports":        "Energetic, Competitive, Exciting",
    "fitness":       "Motivational, Strong, Inspiring",
    "fashion":       "Trendy, Aesthetic, Stylish",
    "technology":    "Modern, Innovative, Smart",
    "travel":        "Adventurous, Free-spirited, Wanderlust",
    "automobile":    "Powerful, Dynamic, Cool",
    "pet":           "Cute, Heartwarming, Fun",
    "nature":        "Peaceful, Beautiful, Serene",
    "entertainment": "Fun, Creative, Viral",
    "education":     "Informative, Intellectual, Valuable",
    "business":      "Professional, Credible, Authoritative",
    "lifestyle":     "Relatable, Everyday, Authentic",
}
 
# category → reel style
CATEGORY_REEL_STYLE = {
    "food":          "Close-up slow pour + ASMR cuts",
    "sports":        "Fast action cuts + slow motion replay",
    "fitness":       "Transformation reveal + fast cuts",
    "fashion":       "Outfit reveal + slow motion walk",
    "technology":    "Screen recording + reaction cuts",
    "travel":        "Time-lapse + wide scenic shots",
    "automobile":    "Dynamic driving shots + cinematic",
    "pet":           "Candid moments + slow motion cute clips",
    "nature":        "Time-lapse + wide landscape shots",
    "entertainment": "Performance cuts + crowd reaction",
    "education":     "Text overlay + talking head",
    "business":      "Clean professional b-roll + talking head",
    "lifestyle":     "Day-in-life montage + voiceover",
}
 
 
def analyze_visual_content(image_path):
    try:
        image         = Image.open(image_path)
        width, height = image.size
        file_size     = os.path.getsize(image_path)
        aspect        = round(width / height, 2)
 
        # YOLO detection
        results     = model(image_path, verbose=False)
        detected    = []
        confidences = []
 
        for result in results:
            for box in result.boxes:
                cls_id     = int(box.cls[0])
                class_name = model.names[cls_id]
                confidence = float(box.conf[0])
                if confidence >= 0.35:
                    detected.append(class_name)
                    confidences.append(confidence)
 
        # deduplicate
        seen, unique = set(), []
        for obj in detected:
            if obj not in seen:
                seen.add(obj)
                unique.append(obj)
        detected_objects = unique
 
        avg_conf = round(sum(confidences)/len(confidences), 2) if confidences else 0.0
 
        # -----------------------------------
        # DETECT PRIMARY CATEGORY
        # from what's actually in the image
        # -----------------------------------
        object_categories = {}
        for obj in detected_objects:
            cat = OBJECT_CATEGORY_MAP.get(obj)
            if cat:
                object_categories[cat] = object_categories.get(cat, 0) + 1
 
        # pick primary category by priority
        primary_category = "lifestyle"
        for cat in CATEGORY_PRIORITY:
            if cat in object_categories:
                primary_category = cat
                break
 
        # special case: person + objects
        has_person = "person" in detected_objects
        if has_person and not object_categories:
            primary_category = "lifestyle"
 
        content_type  = CATEGORY_LABELS.get(primary_category, "Lifestyle Content")
        content_mood  = CATEGORY_MOOD.get(primary_category, "Authentic, Relatable")
        reel_style    = CATEGORY_REEL_STYLE.get(primary_category, "Fast cuts + trending audio")
 
        # -----------------------------------
        # VISUAL SCORE
        # -----------------------------------
        score = 50
        for obj in detected_objects:
            score += OBJECT_SCORES.get(obj, 3)
        if len(detected_objects) >= 3: score += 10
        if len(detected_objects) >= 5: score += 5
        if avg_conf >= 0.75: score += 8
        elif avg_conf >= 0.55: score += 4
        if width >= 1080 and height >= 1080: score += 10
        elif width >= 720 and height >= 720: score += 5
        if 0.54 <= aspect <= 0.57:   score += 8   # 9:16
        elif 0.99 <= aspect <= 1.01: score += 5   # 1:1
        elif 1.74 <= aspect <= 1.78: score += 3   # 16:9
        score = min(score, 100)
 
        # thumbnail quality
        if width >= 1280 and height >= 720 and file_size >= 100_000:
            thumbnail_quality = "Excellent"
        elif width >= 720 and height >= 480:
            thumbnail_quality = "Good"
        elif width >= 480:
            thumbnail_quality = "Average"
        else:
            thumbnail_quality = "Poor — upgrade resolution"
 
        # engagement style
        if has_person and len(detected_objects) >= 3:
            engagement_style = "Very High Human Engagement"
        elif has_person:
            engagement_style = "High Human Engagement"
        elif len(detected_objects) >= 3:
            engagement_style = "Multi-Object Engagement"
        else:
            engagement_style = "Normal Engagement"
 
        # viral potential
        if score >= 85:   viral_potential = "Very High"
        elif score >= 70: viral_potential = "High"
        elif score >= 55: viral_potential = "Medium"
        else:             viral_potential = "Low"
 
        # aspect ratio label
        if 0.54 <= aspect <= 0.57:
            aspect_label = "9:16 Vertical (Reels/Shorts — Best)"
        elif 0.99 <= aspect <= 1.01:
            aspect_label = "1:1 Square (Feed — Good)"
        elif 1.74 <= aspect <= 1.78:
            aspect_label = "16:9 Landscape (YouTube)"
        else:
            aspect_label = f"Custom ({aspect})"
 
        print(f"VISUAL: objects={detected_objects}, category={primary_category}, score={score}")
 
        return {
            "detected_objects":   detected_objects,
            "object_count":       len(detected_objects),
            "avg_confidence":     avg_conf,
            "primary_category":   primary_category,      # KEY FIELD — drives all modules
            "content_type":       content_type,
            "content_mood":       content_mood,
            "recommended_reel_style": reel_style,
            "visual_score":       score,
            "engagement_style":   engagement_style,
            "thumbnail_quality":  thumbnail_quality,
            "viral_potential":    viral_potential,
            "image_resolution":   f"{width}x{height}",
            "aspect_ratio":       aspect_label,
            "has_person":         has_person,
            "all_categories":     list(object_categories.keys()),
        }
 
    except Exception as e:
        print("VISUAL ANALYZER ERROR:", e)
        return {
            "detected_objects":[], "object_count":0, "avg_confidence":0.0,
            "primary_category":"lifestyle", "content_type":"Lifestyle Content",
            "content_mood":"Authentic", "recommended_reel_style":"Fast cuts",
            "visual_score":40, "engagement_style":"Normal", "thumbnail_quality":"Unknown",
            "viral_potential":"Low", "image_resolution":"Unknown",
            "aspect_ratio":"Unknown", "has_person":False, "all_categories":[],
        }
 