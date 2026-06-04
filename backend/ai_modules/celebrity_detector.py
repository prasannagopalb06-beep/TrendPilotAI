import os
 
CELEBRITY_FOLDER = "celebrities"
 
# Use absolute path to avoid path issues
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELEBRITY_FOLDER_ABS = os.path.join(BASE_DIR, "celebrities")
 
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
 
# -----------------------------------
# MODEL THRESHOLDS
# Lower = easier to match (more false positives)
# Higher = stricter (more false negatives)
# For video frames use lower thresholds
# -----------------------------------
THRESHOLDS = {
    "VGG-Face": {"cosine": 0.45, "euclidean": 0.90},
    "Facenet":  {"cosine": 0.40, "euclidean": 10.0},
    "Facenet512":{"cosine": 0.30, "euclidean": 23.56},
    "ArcFace":  {"cosine": 0.68, "euclidean": 4.15},
    "DeepFace": {"cosine": 0.23, "euclidean": 64.0},
}
 
 
def detect_celebrity(image_path):
    try:
        from deepface import DeepFace
        import numpy as np
 
        folder = CELEBRITY_FOLDER_ABS
        if not os.path.exists(folder):
            folder = CELEBRITY_FOLDER
        if not os.path.exists(folder):
            print(f"CELEBRITY FOLDER NOT FOUND: {folder}")
            return _no_detection()
 
        celebrity_files = [
            f for f in os.listdir(folder)
            if f.lower().endswith(VALID_EXTENSIONS)
        ]
 
        if not celebrity_files:
            print("NO CELEBRITY IMAGES IN FOLDER")
            return _no_detection()
 
        print(f"CELEBRITY FOLDER PATH: {folder}")
        print(f"CELEBRITY CHECK: {len(celebrity_files)} images in db")
 
        # -----------------------------------
        # STEP 1: Try DeepFace.find() first
        # Most accurate — uses embedding DB
        # -----------------------------------
        for model_name in ["Facenet512", "ArcFace", "Facenet", "VGG-Face"]:
            try:
                results = DeepFace.find(
                    img_path          = image_path,
                    db_path           = folder,
                    model_name        = model_name,
                    distance_metric   = "cosine",
                    enforce_detection = False,
                    silent            = True
                )
 
                if results and len(results) > 0:
                    df = results[0]
                    if not df.empty:
                        df            = df.sort_values("distance")
                        best_row      = df.iloc[0]
                        best_distance = float(best_row["distance"])
                        best_identity = str(best_row["identity"])
 
                        filename       = os.path.basename(best_identity)
                        celebrity_name = os.path.splitext(filename)[0]
                        confidence     = int((1 - best_distance) * 100)
 
                        threshold = THRESHOLDS.get(model_name, {}).get("cosine", 0.45)
 
                        print(f"FIND [{model_name}]: {celebrity_name} | dist={best_distance:.3f} | conf={confidence}% | threshold={threshold}")
 
                        if best_distance < threshold:
                            return {
                                "celebrity_detected": True,
                                "celebrity_name":     _clean_name(celebrity_name),
                                "confidence":         confidence,
                                "model_used":         model_name,
                                "match_distance":     round(best_distance, 3)
                            }
            except Exception as e:
                print(f"FIND [{model_name}] error: {e}")
                continue
 
        # -----------------------------------
        # STEP 2: Verify loop with multiple models
        # Lower thresholds for video frames
        # -----------------------------------
        print("Trying verify() loop with relaxed thresholds...")
 
        all_scores = {}  # celebrity_name -> list of confidences
 
        for model_name in ["Facenet512", "ArcFace", "Facenet", "VGG-Face"]:
            for file in celebrity_files:
                celeb_image = os.path.join(folder, file)
                celeb_name  = os.path.splitext(file)[0]
 
                try:
                    result = DeepFace.verify(
                        img1_path         = image_path,
                        img2_path         = celeb_image,
                        model_name        = model_name,
                        distance_metric   = "cosine",
                        enforce_detection = False,
                        silent            = True
                    )
 
                    distance   = result["distance"]
                    confidence = int((1 - distance) * 100)
 
                    print(f"  {file} [{model_name}]: dist={distance:.3f} conf={confidence}%")
 
                    if celeb_name not in all_scores:
                        all_scores[celeb_name] = []
                    all_scores[celeb_name].append(confidence)
 
                except Exception as e:
                    print(f"  VERIFY ERROR {file} [{model_name}]: {e}")
                    continue
 
        # -----------------------------------
        # STEP 3: Average scores across models
        # and pick best celebrity
        # -----------------------------------
        if all_scores:
            # compute average confidence per celebrity
            avg_scores = {
                name: sum(scores) / len(scores)
                for name, scores in all_scores.items()
            }
            best_celeb = max(avg_scores, key=avg_scores.get)
            best_avg   = avg_scores[best_celeb]
            best_max   = max(all_scores[best_celeb])
 
            print(f"\nBEST MATCH: {best_celeb} | avg={best_avg:.1f}% | max={best_max}%")
            print(f"ALL AVERAGES: {avg_scores}")
 
            # Use relaxed threshold for video frames
            # (video frames are lower quality than photos)
            DETECT_THRESHOLD = 40  # detect if avg confidence > 40%
 
            if best_avg >= DETECT_THRESHOLD:
                return {
                    "celebrity_detected": True,
                    "celebrity_name":     _clean_name(best_celeb),
                    "confidence":         int(best_avg),
                    "max_confidence":     best_max,
                    "model_used":         "multi-model average",
                    "all_scores":         {k: round(v, 1) for k, v in avg_scores.items()}
                }
 
            # Even lower fallback — if max confidence from any model > 50%
            if best_max >= 50:
                return {
                    "celebrity_detected": True,
                    "celebrity_name":     _clean_name(best_celeb),
                    "confidence":         best_max,
                    "max_confidence":     best_max,
                    "model_used":         "best-model match",
                    "note":               "Low confidence match — verify manually"
                }
 
        print(f"NO CELEBRITY MATCHED")
        return {
            "celebrity_detected": False,
            "celebrity_name":     None,
            "confidence":         int(max(max(v) for v in all_scores.values())) if all_scores else 0
        }
 
    except ImportError:
        print("DEEPFACE NOT INSTALLED")
        return _no_detection()
 
    except Exception as e:
        print(f"CELEBRITY DETECTOR ERROR: {e}")
        return _no_detection()
 
 
def _clean_name(name):
    """vijay → Vijay, sharukkhan → Sharukkhan"""
    return name.replace("_", " ").replace("-", " ").title()
 
 
def _no_detection():
    return {
        "celebrity_detected": False,
        "celebrity_name":     None,
        "confidence":         0
    }