from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
 
from ai_modules.visual_analyzer      import analyze_visual_content
from ai_modules.trend_analyzer       import get_realtime_trends
from ai_modules.music_analyzer       import recommend_music
from ai_modules.hashtag_generator    import generate_hashtags
from ai_modules.caption_analyzer     import analyze_caption
from ai_modules.engagement_predictor import predict_engagement
from ai_modules.platform_strategy    import generate_platform_strategy
from ai_modules.region_analyzer      import analyze_region
from ai_modules.celebrity_detector   import detect_celebrity
from ai_modules.video_frame_extractor import get_analysis_image
 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
 
def generate_final_report(image_path, caption="", region="IN",
                           state="", platforms=None, goal="viral"):
    if platforms is None:
        platforms = ["instagram"]
 
    try:
 
        # ── EXTRACT FRAME IF VIDEO ────────────────────────────────────────
        analysis_image = get_analysis_image(image_path)
        if analysis_image is None:
            print("No image available for analysis — using caption only")
            analysis_image = image_path  # fallback, modules will handle error
 
        print(f"\nANALYSIS IMAGE: {analysis_image}")
 
        # ── STEP 1: VISUAL (runs first — drives everything) ──────────────
        try:
            visual_data = analyze_visual_content(analysis_image)
        except Exception as e:
            print("VISUAL ERROR:", e)
            visual_data = {
                "detected_objects":[], "object_count":0, "avg_confidence":0.0,
                "primary_category":"lifestyle", "content_type":"Lifestyle Content",
                "content_mood":"Authentic", "recommended_reel_style":"Fast cuts",
                "visual_score":50, "engagement_style":"Normal",
                "thumbnail_quality":"Unknown", "viral_potential":"Low",
                "image_resolution":"Unknown", "aspect_ratio":"Unknown",
                "has_person":False, "all_categories":[],
            }
        print("\nVISUAL DATA:\n", visual_data)
 
        # PRIMARY CATEGORY from visual — this drives ALL modules
        primary_category = visual_data.get("primary_category", "lifestyle")
        print(f"\n>>> PRIMARY CATEGORY (from image): {primary_category}")
 
        # ── STEP 2: CELEBRITY ────────────────────────────────────────────
        try:
            celebrity_data = detect_celebrity(analysis_image)
        except Exception as e:
            print("CELEBRITY ERROR:", e)
            celebrity_data = {"celebrity_detected":False,"celebrity_name":None,"confidence":0}
        print("\nCELEBRITY DATA:\n", celebrity_data)
 
        # ── STEP 3: CAPTION (supplements visual, doesn't override) ───────
        try:
            caption_data = analyze_caption(caption)
        except Exception as e:
            print("CAPTION ERROR:", e)
            caption_data = {"original_caption":caption,"keywords":[],"emotion":"general",
                            "caption_length":len(caption),"word_count":0,
                            "has_hashtags":False,"has_emojis":False,"caption_quality":"Unknown"}
        print("\nCAPTION DATA:\n", caption_data)
 
        # ── STEP 4: TREND KEYWORD ────────────────────────────────────────
        # Priority: celebrity > visual primary category > caption keyword
        if celebrity_data.get("celebrity_detected"):
            trend_keyword = celebrity_data["celebrity_name"]
        else:
            # Use visual primary category as the main keyword
            trend_keyword = primary_category
            # Refine with caption keyword if it matches visual category
            cap_keywords = caption_data.get("keywords", [])
            if cap_keywords:
                first_kw = cap_keywords[0].lower()
                # only use caption keyword if it's related to visual
                RELATED = {
                    "food":["food","cook","recipe","eat","chef","restaurant"],
                    "sports":["sport","cricket","football","game","match","ipl"],
                    "fitness":["gym","workout","fitness","training","exercise"],
                    "fashion":["fashion","style","ootd","outfit","clothes","dress"],
                    "travel":["travel","trip","tour","vacation","explore"],
                    "technology":["tech","ai","code","gadget","laptop","phone"],
                    "pet":["dog","cat","pet","animal"],
                    "motivation":["motivation","inspire","hustle","success","mindset"],
                }
                related_words = RELATED.get(primary_category, [])
                if any(r in first_kw for r in related_words):
                    trend_keyword = first_kw
 
        try:
            trend_data = get_realtime_trends(
                keyword=trend_keyword, region=region, state=state,
                visual_category=primary_category
            )
        except Exception as e:
            print("TREND ERROR:", e)
            trend_data = {"main_keyword":trend_keyword,"category":primary_category,
                          "trending_topics":[],"trend_strength":"Unknown",
                          "hashtags":["#Trending","#Viral","#FYP"],
                          "regional_songs":[],"sources_used":[]}
        print("\nTREND DATA:\n", trend_data)
 
        # ── STEP 5: MUSIC (based on visual category + state) ─────────────
        try:
            music_data = recommend_music(
                visual_data, caption_data, trend_data, region=region
            )
        except Exception as e:
            print("MUSIC ERROR:", e)
            music_data = {"recommended_songs":["Trending Audio"],"music_category":primary_category,
                          "music_strategy":{"best_reel_style":visual_data.get("recommended_reel_style","Fast cuts"),
                                            "recommended_platform":"Instagram Reels",
                                            "viral_audio_probability":"Medium"}}
        print("\nMUSIC DATA:\n", music_data)
 
        # ── STEP 6: HASHTAGS (based on visual category + state) ──────────
        try:
            hashtag_data = generate_hashtags(
                visual_data, caption_data, trend_data, region=region
            )
        except Exception as e:
            print("HASHTAG ERROR:", e)
            hashtag_data = {"recommended_hashtags":["#Trending","#Viral","#FYP"],
                            "hashtag_strategy":{"best_count":"12-18","best_mix":"Mixed","algorithm_boost":"Medium"}}
        print("\nHASHTAG DATA:\n", hashtag_data)
 
        # ── STEP 7: REGION ───────────────────────────────────────────────
        try:
            region_data = analyze_region(region, visual_data, caption_data, trend_data)
        except Exception as e:
            print("REGION ERROR:", e)
            region_data = {"region":"India","languages":["English"],"best_upload_time":"7 PM - 10 PM",
                           "audience_behavior":"Unknown","regional_viral_score":50,"audience_match_score":50}
        print("\nREGION DATA:\n", region_data)
 
        # ── STEP 8: ENGAGEMENT ───────────────────────────────────────────
        try:
            engagement_data = predict_engagement(visual_data, caption_data, trend_data, music_data)
        except Exception as e:
            print("ENGAGEMENT ERROR:", e)
            engagement_data = {"engagement_score":50,"engagement_probability":"Medium",
                               "estimated_reach":"Moderate Reach","best_engagement_factor":"Visual Quality",
                               "improvement_tips":[],"score_breakdown":{}}
        print("\nENGAGEMENT DATA:\n", engagement_data)
 
        # ── STEP 9: PLATFORM ─────────────────────────────────────────────
        try:
            platform_data = generate_platform_strategy(
                visual_data, caption_data, trend_data,
                engagement_data, music_data, region=region
            )
        except Exception as e:
            print("PLATFORM ERROR:", e)
            platform_data = {"best_platform":"Instagram Reels","viral_level":"Medium",
                             "best_upload_time":"7 PM - 10 PM","recommended_content_style":"Short reels",
                             "recommended_posting_frequency":"1-2 daily",
                             "best_video_duration":"15-30 seconds","strategy_tips":[]}
        print("\nPLATFORM STRATEGY:\n", platform_data)
 
        # ── STEP 10: AI CAPTION ──────────────────────────────────────────
        try:
            platforms_str = ", ".join(platforms)
            caption_prompt = f"""You are a viral social media caption expert.
 
WHAT IS IN THE IMAGE (from AI vision analysis):
- Detected Objects: {visual_data.get('detected_objects')}
- Content Category: {visual_data.get('content_type')}
- Content Mood: {visual_data.get('content_mood')}
- Has Person: {visual_data.get('has_person')}
 
User Caption: {caption_data.get('original_caption') or 'No caption provided'}
Keywords from caption: {caption_data.get('keywords')}
Trending Topics: {trend_data.get('trending_topics')}
Region: {region}{f' / State: {state}' if state else ''}
User's Platforms: {platforms_str}
User's Goal: {goal}
Top Hashtags: {hashtag_data.get('recommended_hashtags', [])[:8]}
Celebrity: {celebrity_data.get('celebrity_name') if celebrity_data.get('celebrity_detected') else 'None'}
 
Write exactly 3 captions based on WHAT IS ACTUALLY IN THE IMAGE above.
No explanations. No asterisks. No placeholders. No fake content.
 
INSTAGRAM:
(max 150 chars, 3-5 emojis relevant to the image content, CTA at end)
 
YOUTUBE:
(max 200 chars, keyword-rich based on actual image content, no emojis)
 
HOOK:
(max 50 chars, punchy single line based on what's in the image)"""
 
            cap_resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role":"system","content":"Write short punchy captions based ONLY on the actual image content provided. Never invent content."},
                    {"role":"user","content":caption_prompt}
                ],
                temperature=0.85, max_tokens=300
            )
            ai_caption_data = {"generated_caption": cap_resp.choices[0].message.content}
        except Exception as e:
            print("AI CAPTION ERROR:", e)
            ai_caption_data = {"generated_caption": "Caption generation failed."}
        print("\nAI CAPTION:\n", ai_caption_data)
 
        # ── STEP 11: FINAL REPORT ────────────────────────────────────────
        celeb_context = (
            f"Celebrity Detected: {celebrity_data['celebrity_name']} ({celebrity_data['confidence']}% confidence)"
            if celebrity_data.get("celebrity_detected")
            else "No celebrity detected."
        )
 
        final_prompt = f"""You are TrendPilotAI — an expert AI social media strategist.
 
Analyze the following data and generate a professional report.
 
CRITICAL RULES:
- Base ALL analysis on VISUAL DATA — what was actually detected in the image
- Do NOT hallucinate objects, people, or celebrities
- Only mention celebrity if confirmed in CELEBRITY section
- No markdown bold (**) or asterisks
- No placeholders
 
===== WHAT AI SAW IN THE IMAGE =====
Detected Objects: {visual_data.get('detected_objects')}
Primary Category: {visual_data.get('primary_category')}
Content Type: {visual_data.get('content_type')}
Content Mood: {visual_data.get('content_mood')}
Has Person: {visual_data.get('has_person')}
Visual Score: {visual_data.get('visual_score')}/100
Viral Potential: {visual_data.get('viral_potential')}
Recommended Reel Style: {visual_data.get('recommended_reel_style')}
Resolution: {visual_data.get('image_resolution')}
Aspect Ratio: {visual_data.get('aspect_ratio')}
 
===== CELEBRITY =====
{celeb_context}
 
===== CAPTION =====
{caption_data}
 
===== TRENDS (based on visual category) =====
{trend_data}
 
===== MUSIC (matched to visual content) =====
{music_data}
 
===== HASHTAGS (matched to visual content) =====
{hashtag_data}
 
===== REGION =====
Region: {region}{f', State: {state}' if state else ''}
{region_data}
 
===== ENGAGEMENT =====
{engagement_data}
 
===== PLATFORM =====
User's Platforms: {", ".join(platforms)}
User's Goal: {goal}
{platform_data}
 
===== AI CAPTIONS =====
{ai_caption_data}
 
===== GENERATE REPORT =====
 
1. Virality Score (/10) — based on visual + trend + engagement data
2. What's In The Image — describe what AI detected and its viral potential
3. Content Category & Mood Analysis
4. Celebrity / Person Impact (only if detected)
5. Caption Quality — based on user's caption vs visual content
6. Trend Match — how the visual content matches current trends
7. Best Platform for this exact content — from user's selected platforms: {", ".join(platforms)}
8. Upload Time & Day
9. Music Strategy — songs matched to the visual content category
10. Hashtag Breakdown — viral / niche / regional tiers
11. Engagement Forecast
12. 3 Specific Growth Actions for this exact content
13. Final Verdict
 
Use headings and bullets. Be specific to the actual image content."""
 
        final_resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system","content":"Expert AI social media strategist. Always base analysis on the actual detected image content."},
                {"role":"user","content":final_prompt}
            ],
            temperature=0.7, max_tokens=2000
        )
        final_report = final_resp.choices[0].message.content
 
        return {
            "success":               True,
            "visual_analysis":       visual_data,
            "celebrity_detection":   celebrity_data,
            "caption_analysis":      caption_data,
            "trend_analysis":        trend_data,
            "music_recommendation":  music_data,
            "hashtag_strategy":      hashtag_data,
            "region_analysis":       region_data,
            "engagement_prediction": engagement_data,
            "platform_strategy":     platform_data,
            "ai_caption_generation": ai_caption_data,
            "final_report":          final_report,
        }
 
    except Exception as e:
        print("\nFINAL ANALYZER ERROR:", e)
        return {"success": False, "error": str(e)}