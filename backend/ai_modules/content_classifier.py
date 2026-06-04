def classify_content(visual_data, caption):

    caption = caption.lower()

    labels = []

    # -----------------------------
    # CAPTION ANALYSIS
    # -----------------------------

    if any(word in caption for word in [
        "happy", "smile", "joy", "peace"
    ]):
        labels.append("positive")

    if any(word in caption for word in [
        "travel", "vacation", "trip", "beach"
    ]):
        labels.append("travel")

    if any(word in caption for word in [
        "fashion", "style", "outfit"
    ]):
        labels.append("fashion")

    if any(word in caption for word in [
        "gym", "fitness", "workout"
    ]):
        labels.append("fitness")

    if any(word in caption for word in [
        "cinema", "movie", "actor"
    ]):
        labels.append("cinematic")

    # -----------------------------
    # VISUAL ANALYSIS
    # -----------------------------

    aesthetic_score = visual_data.get(
        "aesthetic_score",
        5
    )

    color_style = visual_data.get(
        "color_style",
        ""
    )

    if aesthetic_score >= 7:
        labels.append("aesthetic")

    if "pastel" in color_style.lower():
        labels.append("instagram_style")

    # -----------------------------
    # FINAL DEFAULT
    # -----------------------------

    if len(labels) == 0:
        labels.append("general")

    return {
        "content_labels": labels
    }