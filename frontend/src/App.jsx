import { useState } from "react";
import axios from "axios";

const INDIA_STATES = [
  { code:"IN-TN", name:"Tamil Nadu",       flag:"🏛️" },
  { code:"IN-MH", name:"Maharashtra",      flag:"🏙️" },
  { code:"IN-KA", name:"Karnataka",        flag:"🌿" },
  { code:"IN-AP", name:"Andhra Pradesh",   flag:"🌾" },
  { code:"IN-TS", name:"Telangana",        flag:"🌆" },
  { code:"IN-KL", name:"Kerala",           flag:"🌴" },
  { code:"IN-DL", name:"Delhi",            flag:"🏛️" },
  { code:"IN-UP", name:"Uttar Pradesh",    flag:"🕌" },
  { code:"IN-GJ", name:"Gujarat",          flag:"🎪" },
  { code:"IN-RJ", name:"Rajasthan",        flag:"🏰" },
  { code:"IN-PB", name:"Punjab",           flag:"🌾" },
  { code:"IN-WB", name:"West Bengal",      flag:"🎨" },
  { code:"IN-OR", name:"Odisha",           flag:"🛕" },
  { code:"IN-BR", name:"Bihar",            flag:"🌻" },
  { code:"IN-AS", name:"Assam",            flag:"🍃" },
  { code:"IN-HP", name:"Himachal Pradesh", flag:"🏔️" },
  { code:"IN-GA", name:"Goa",              flag:"🏖️" },
];

const PLATFORMS = [
  { id:"instagram", name:"Instagram Reels", icon:"📸" },
  { id:"youtube",   name:"YouTube Shorts",  icon:"▶️"  },
  { id:"facebook",  name:"Facebook Reels",  icon:"👥"  },
  { id:"tiktok",    name:"TikTok",          icon:"🎵"  },
  { id:"twitter",   name:"Twitter/X",       icon:"🐦"  },
  { id:"snapchat",  name:"Snapchat",        icon:"👻"  },
];

const CONTENT_GOALS = [
  { id:"viral",    label:"Go Viral",        icon:"🔥" },
  { id:"brand",    label:"Brand Awareness", icon:"💼" },
  { id:"engage",   label:"Max Engagement",  icon:"❤️" },
  { id:"follower", label:"Grow Followers",  icon:"📈" },
  { id:"sales",    label:"Drive Sales",     icon:"💰" },
];

const TABS = [
  { id:"trends",   label:"Trends",   icon:"📈" },
  { id:"visual",   label:"Visual",   icon:"👁️" },
  { id:"music",    label:"Music",    icon:"🎵" },
  { id:"hashtags", label:"Hashtags", icon:"#️⃣" },
  { id:"platform", label:"Platform", icon:"🏆" },
  { id:"region",   label:"Region",   icon:"🌍" },
  { id:"captions", label:"Captions", icon:"🤖" },
  { id:"report",   label:"Report",   icon:"📋" },
];

export default function App() {
  const [file,      setFile]      = useState(null);
  const [caption,   setCaption]   = useState("");
  const [country,   setCountry]   = useState("IN");
  const [state,     setState]     = useState("");
  const [platforms, setPlatforms] = useState(["instagram"]);
  const [goal,      setGoal]      = useState("viral");
  const [loading,   setLoading]   = useState(false);
  const [result,    setResult]    = useState(null);
  const [preview,   setPreview]   = useState(null);
  const [activeTab, setActiveTab] = useState("trends");

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    setFile(f);
    if (f && f.type.startsWith("image/")) setPreview(URL.createObjectURL(f));
  };

  const togglePlatform = (id) =>
    setPlatforms(prev =>
      prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id]
    );

  const handleSubmit = async () => {
    if (!file) { alert("Upload image or video"); return; }
    if (platforms.length === 0) { alert("Select at least one platform"); return; }
    try {
      setLoading(true);
      setResult(null);
      const fd = new FormData();
      fd.append("file",      file);
      fd.append("caption",   caption);
      fd.append("region",    country);
      fd.append("state",     state);
      fd.append("platforms", platforms.join(","));
      fd.append("goal",      goal);
      const res = await axios.post("http://127.0.0.1:8000/analyze", fd,
        { headers: { "Content-Type": "multipart/form-data" } });
      setResult(res.data.data);
    } catch (err) {
      console.error(err);
      alert("Backend Error — check terminal");
    } finally {
      setLoading(false);
    }
  };

  const stateInfo = INDIA_STATES.find(s => s.code === state);

  // ── Helpers ────────────────────────────────────────────────────
  const Card = ({ title, icon, children, accent = "#06b6d4" }) => (
    <div style={{ background:"#1e293b", borderRadius:"12px", padding:"20px",
      border:"1px solid #334155", borderTop:`3px solid ${accent}` }}>
      <h3 style={{ color:accent, marginTop:0, marginBottom:"14px", fontSize:"13px",
        textTransform:"uppercase", letterSpacing:"0.5px" }}>
        {icon} {title}
      </h3>
      {children}
    </div>
  );

  const Row = ({ label, value }) => {
    if (value === null || value === undefined || value === "") return null;
    const display = Array.isArray(value) ? value.join(", ") : String(value);
    return (
      <p style={{ margin:"5px 0", fontSize:"13px" }}>
        <span style={{ color:"#94a3b8" }}>{label}: </span>
        <span style={{ color:"#f1f5f9" }}>{display}</span>
      </p>
    );
  };

  const Tag = ({ text, color = "#06b6d4" }) => (
    <span style={{ display:"inline-block", background:`${color}22`, color,
      border:`1px solid ${color}44`, borderRadius:"99px", padding:"3px 10px",
      fontSize:"12px", margin:"3px 3px 3px 0" }}>
      {text}
    </span>
  );

  const ScoreBar = ({ label, value, max = 100, color = "#06b6d4" }) => (
    <div style={{ marginBottom:"10px" }}>
      <div style={{ display:"flex", justifyContent:"space-between", fontSize:"12px", marginBottom:"4px" }}>
        <span style={{ color:"#94a3b8" }}>{label}</span>
        <span style={{ color, fontWeight:600 }}>{value}/{max}</span>
      </div>
      <div style={{ background:"#0f172a", borderRadius:"99px", height:"7px" }}>
        <div style={{ background:color, width:`${Math.min((value/max)*100,100)}%`,
          height:"7px", borderRadius:"99px", transition:"width 0.6s ease" }} />
      </div>
    </div>
  );

  const r  = result;
  const vd = r?.visual_analysis;
  const cd = r?.caption_analysis;
  const td = r?.trend_analysis;
  const md = r?.music_recommendation;
  const hd = r?.hashtag_strategy;
  const rd = r?.region_analysis;
  const ed = r?.engagement_prediction;
  const pd = r?.platform_strategy;
  const cb = r?.celebrity_detection;
  const ac = r?.ai_caption_generation;

  return (
    <div style={{ background:"#0f172a", minHeight:"100vh", padding:"20px",
      color:"white", fontFamily:"'Segoe UI',Arial,sans-serif" }}>

      {/* Header */}
      <div style={{ textAlign:"center", marginBottom:"28px" }}>
        <h1 style={{ color:"#06b6d4", fontSize:"26px", margin:0, fontWeight:700 }}>
          🚀 TrendPilot AI
        </h1>
        <p style={{ color:"#64748b", fontSize:"13px", margin:"4px 0 0" }}>
          Real-time Social Media Trend Analyzer · Free · For Influencers
        </p>
      </div>

      {/* Upload Panel */}
      <div style={{ background:"#1e293b", padding:"24px", borderRadius:"14px",
        maxWidth:"780px", margin:"auto", border:"1px solid #334155" }}>

        {/* File */}
        <div style={{ display:"flex", gap:"16px", alignItems:"flex-start", flexWrap:"wrap" }}>
          <div style={{ flex:1, minWidth:"220px" }}>
            <label style={{ color:"#94a3b8", fontSize:"12px", display:"block", marginBottom:"6px" }}>
              📸 IMAGE / VIDEO
            </label>
            <input type="file" accept="image/*,video/*" onChange={handleFileChange}
              style={{ color:"#f1f5f9", fontSize:"13px", width:"100%" }} />
          </div>
          {preview && (
            <img src={preview} alt="preview"
              style={{ width:"100px", height:"100px", objectFit:"cover",
                borderRadius:"8px", border:"1px solid #334155" }} />
          )}
        </div>

        {/* Caption */}
        <div style={{ marginTop:"14px" }}>
          <label style={{ color:"#94a3b8", fontSize:"12px", display:"block", marginBottom:"6px" }}>
            ✍️ CAPTION / DESCRIBE YOUR CONTENT
          </label>
          <textarea
            placeholder="e.g. morning gym workout, Tamil fashion reel, street food vlog..."
            value={caption} onChange={e => setCaption(e.target.value)}
            style={{ width:"100%", height:"72px", padding:"10px", boxSizing:"border-box",
              background:"#0f172a", color:"white", border:"1px solid #334155",
              borderRadius:"8px", fontSize:"13px", resize:"vertical" }} />
        </div>

        {/* Country + State */}
        <div style={{ display:"flex", gap:"12px", marginTop:"14px", flexWrap:"wrap" }}>
          <div style={{ flex:1, minWidth:"140px" }}>
            <label style={{ color:"#94a3b8", fontSize:"12px", display:"block", marginBottom:"6px" }}>
              🌍 COUNTRY
            </label>
            <select value={country} onChange={e => { setCountry(e.target.value); setState(""); }}
              style={{ width:"100%", padding:"9px 12px", borderRadius:"8px",
                background:"#0f172a", color:"white", border:"1px solid #334155", fontSize:"13px" }}>
              <option value="IN">🇮🇳 India</option>
              <option value="US">🇺🇸 USA</option>
              <option value="GB">🇬🇧 UK</option>
              <option value="AU">🇦🇺 Australia</option>
            </select>
          </div>

          {country === "IN" && (
            <div style={{ flex:2, minWidth:"200px" }}>
              <label style={{ color:"#94a3b8", fontSize:"12px", display:"block", marginBottom:"6px" }}>
                🏛️ STATE (for regional songs & hashtags)
              </label>
              <select value={state} onChange={e => setState(e.target.value)}
                style={{ width:"100%", padding:"9px 12px", borderRadius:"8px",
                  background:"#0f172a", color:"white", border:"1px solid #334155", fontSize:"13px" }}>
                <option value="">All India</option>
                {INDIA_STATES.map(s => (
                  <option key={s.code} value={s.code}>{s.flag} {s.name}</option>
                ))}
              </select>
              {stateInfo && (
                <p style={{ color:"#06b6d4", fontSize:"11px", margin:"4px 0 0" }}>
                  🎵 Regional songs & hashtags for {stateInfo.name}
                </p>
              )}
            </div>
          )}
        </div>

        {/* Platforms */}
        <div style={{ marginTop:"16px" }}>
          <label style={{ color:"#94a3b8", fontSize:"12px", display:"block", marginBottom:"8px" }}>
            📱 TARGET PLATFORMS
          </label>
          <div style={{ display:"flex", gap:"8px", flexWrap:"wrap" }}>
            {PLATFORMS.map(p => (
              <button key={p.id} onClick={() => togglePlatform(p.id)}
                style={{ padding:"7px 14px", borderRadius:"99px", border:"1px solid",
                  fontSize:"12px", cursor:"pointer",
                  background: platforms.includes(p.id) ? "#0ea5e922" : "transparent",
                  borderColor: platforms.includes(p.id) ? "#0ea5e9" : "#334155",
                  color: platforms.includes(p.id) ? "#0ea5e9" : "#64748b" }}>
                {p.icon} {p.name}
              </button>
            ))}
          </div>
        </div>

        {/* Goal */}
        <div style={{ marginTop:"16px" }}>
          <label style={{ color:"#94a3b8", fontSize:"12px", display:"block", marginBottom:"8px" }}>
            🎯 CONTENT GOAL
          </label>
          <div style={{ display:"flex", gap:"8px", flexWrap:"wrap" }}>
            {CONTENT_GOALS.map(g => (
              <button key={g.id} onClick={() => setGoal(g.id)}
                style={{ padding:"7px 14px", borderRadius:"99px", border:"1px solid",
                  fontSize:"12px", cursor:"pointer",
                  background: goal === g.id ? "#f59e0b22" : "transparent",
                  borderColor: goal === g.id ? "#f59e0b" : "#334155",
                  color: goal === g.id ? "#f59e0b" : "#64748b" }}>
                {g.icon} {g.label}
              </button>
            ))}
          </div>
        </div>

        {/* Submit */}
        <button onClick={handleSubmit} disabled={loading}
          style={{ marginTop:"18px", width:"100%", padding:"14px",
            background: loading ? "#475569" : "linear-gradient(135deg,#0ea5e9,#06b6d4)",
            color:"white", border:"none", borderRadius:"10px", fontSize:"15px",
            fontWeight:700, cursor: loading ? "not-allowed" : "pointer" }}>
          {loading ? "⏳ Analyzing... (15-20 seconds)" : "🔍 Analyze My Content"}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div style={{ marginTop:"32px", maxWidth:"1200px", marginInline:"auto" }}>

          {/* Celebrity Banner */}
          {cb?.celebrity_detected && (
            <div style={{ background:"linear-gradient(135deg,#1e1b4b,#312e81)",
              border:"1px solid #6366f1", borderRadius:"12px", padding:"18px 24px",
              marginBottom:"16px", display:"flex", alignItems:"center", gap:"16px" }}>
              <span style={{ fontSize:"44px" }}>🌟</span>
              <div>
                <p style={{ margin:0, color:"#a5b4fc", fontSize:"12px" }}>Celebrity Detected</p>
                <p style={{ margin:"4px 0 0", color:"#e0e7ff", fontSize:"22px", fontWeight:700 }}>
                  {cb.celebrity_name}
                </p>
                <p style={{ margin:"4px 0 0", color:"#818cf8", fontSize:"13px" }}>
                  Confidence: {cb.confidence}%
                </p>
              </div>
            </div>
          )}

          {/* Quick Stats */}
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(130px,1fr))",
            gap:"10px", marginBottom:"16px" }}>
            {[
              { label:"Visual Score",   value:`${vd?.visual_score||0}/100`,            color:"#06b6d4", icon:"👁️" },
              { label:"Engagement",     value:`${ed?.engagement_score||0}/100`,         color:"#f59e0b", icon:"📊" },
              { label:"Viral Score",    value:`${rd?.regional_viral_score||0}/100`,     color:"#10b981", icon:"🔥" },
              { label:"Trend Strength", value:td?.trend_strength||"—",                  color:"#8b5cf6", icon:"📈" },
              { label:"Best Platform",  value:pd?.best_platform||"—",                   color:"#ec4899", icon:"🏆" },
              { label:"Best Time",      value:pd?.best_upload_time||"—",                color:"#f59e0b", icon:"⏰" },
            ].map((s,i) => (
              <div key={i} style={{ background:"#1e293b", borderRadius:"10px", padding:"14px",
                border:"1px solid #334155", textAlign:"center" }}>
                <div style={{ fontSize:"18px" }}>{s.icon}</div>
                <div style={{ color:s.color, fontWeight:700, fontSize:"14px", margin:"4px 0 2px" }}>
                  {s.value}
                </div>
                <div style={{ color:"#64748b", fontSize:"11px" }}>{s.label}</div>
              </div>
            ))}
          </div>

          {/* Sources */}
          {td?.sources_used?.length > 0 && (
            <div style={{ background:"#1e293b", border:"1px solid #334155", borderRadius:"10px",
              padding:"10px 16px", marginBottom:"16px", display:"flex", gap:"8px",
              flexWrap:"wrap", alignItems:"center" }}>
              <span style={{ color:"#64748b", fontSize:"12px" }}>Live data from:</span>
              {td.sources_used.map((s,i) => <Tag key={i} text={`✅ ${s}`} color="#10b981" />)}
            </div>
          )}

          {/* Tabs */}
          <div style={{ display:"flex", gap:"4px", marginBottom:"16px",
            overflowX:"auto", paddingBottom:"4px" }}>
            {TABS.map(t => (
              <button key={t.id} onClick={() => setActiveTab(t.id)}
                style={{ padding:"8px 14px", borderRadius:"8px", border:"1px solid",
                  fontSize:"12px", cursor:"pointer", whiteSpace:"nowrap",
                  background: activeTab===t.id ? "#0ea5e922" : "transparent",
                  borderColor: activeTab===t.id ? "#0ea5e9" : "#334155",
                  color: activeTab===t.id ? "#0ea5e9" : "#64748b" }}>
                {t.icon} {t.label}
              </button>
            ))}
          </div>

          {/* TAB: TRENDS */}
          {activeTab === "trends" && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))", gap:"16px" }}>
              <Card title="Google + YouTube Trends" icon="📈" accent="#10b981">
                <Row label="Keyword"  value={td?.main_keyword} />
                <Row label="Category" value={td?.category} />
                <Row label="Strength" value={td?.trend_strength} />
                <div style={{ marginTop:"10px" }}>
                  <p style={{ color:"#10b981", fontSize:"12px", margin:"0 0 6px" }}>🔥 Trending Topics:</p>
                  {(td?.trending_topics||[]).map((t,i) => <Tag key={i} text={t} color="#10b981" />)}
                </div>
                {td?.youtube_trending_videos?.length > 0 && (
                  <div style={{ marginTop:"12px" }}>
                    <p style={{ color:"#ef4444", fontSize:"12px", margin:"0 0 6px" }}>▶️ YouTube Trending Now:</p>
                    {td.youtube_trending_videos.map((v,i) => (
                      <div key={i} style={{ marginBottom:"6px" }}>
                        <a href={v.url} target="_blank" rel="noreferrer"
                          style={{ color:"#f1f5f9", fontSize:"12px" }}>🎬 {v.title}</a>
                        <span style={{ color:"#64748b", fontSize:"11px" }}> — {v.channel}</span>
                      </div>
                    ))}
                  </div>
                )}
              </Card>

              <Card title="Instagram Trend Intelligence" icon="📱" accent="#ec4899">
                <div style={{ marginBottom:"10px" }}>
                  <p style={{ color:"#ec4899", fontSize:"12px", margin:"0 0 6px" }}>🔥 Mega Tags:</p>
                  {(td?.instagram_mega_tags||[]).map((t,i) => <Tag key={i} text={t} color="#ec4899" />)}
                </div>
                <div style={{ marginBottom:"10px" }}>
                  <p style={{ color:"#f59e0b", fontSize:"12px", margin:"0 0 6px" }}>🎯 Niche Tags:</p>
                  {(td?.instagram_niche_tags||[]).map((t,i) => <Tag key={i} text={t} color="#f59e0b" />)}
                </div>
                <div>
                  <p style={{ color:"#10b981", fontSize:"12px", margin:"0 0 6px" }}>🚀 Rising Tags:</p>
                  {(td?.instagram_rising_tags||[]).map((t,i) => <Tag key={i} text={t} color="#10b981" />)}
                </div>
              </Card>

              <Card title="Your Platform Tips" icon="💡" accent="#8b5cf6">
                {platforms.map(pid => {
                  const pf = PLATFORMS.find(p => p.id === pid);
                  return (
                    <div key={pid} style={{ marginBottom:"12px", padding:"10px",
                      background:"#0f172a", borderRadius:"8px" }}>
                      <p style={{ color:"#8b5cf6", fontSize:"13px", margin:"0 0 6px", fontWeight:600 }}>
                        {pf?.icon} {pf?.name}
                      </p>
                      {(pd?.strategy_tips||[]).slice(0,3).map((tip,i) => (
                        <p key={i} style={{ color:"#94a3b8", fontSize:"12px", margin:"3px 0" }}>• {tip}</p>
                      ))}
                    </div>
                  );
                })}
              </Card>
            </div>
          )}

          {/* TAB: VISUAL */}
          {activeTab === "visual" && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))", gap:"16px" }}>
              <Card title="Visual Analysis" icon="👁️" accent="#06b6d4">
                <ScoreBar label="Visual Score" value={vd?.visual_score||0} color="#06b6d4" />
                <Row label="Content Type"     value={vd?.content_type} />
                <Row label="Content Mood"     value={vd?.content_mood} />
                <Row label="Detected Objects" value={vd?.detected_objects} />
                <Row label="Object Count"     value={vd?.object_count} />
                <Row label="Resolution"       value={vd?.image_resolution} />
                <Row label="Aspect Ratio"     value={vd?.aspect_ratio} />
                <Row label="Thumbnail"        value={vd?.thumbnail_quality} />
                <Row label="Viral Potential"  value={vd?.viral_potential} />
                <Row label="Reel Style"       value={vd?.recommended_reel_style} />
              </Card>

              <Card title="Content Feel & Mood" icon="🎭" accent="#ec4899">
                <Row label="Visual Category"  value={vd?.primary_category} />
                <Row label="Content Mood"     value={vd?.content_mood} />
                <Row label="Caption Emotion"  value={cd?.emotion} />
                <Row label="Caption Quality"  value={cd?.caption_quality} />
                <Row label="Keywords"         value={cd?.keywords} />
                <Row label="Has Hashtags"     value={cd?.has_hashtags ? "✅ Yes" : "❌ No"} />
                <Row label="Has Emojis"       value={cd?.has_emojis ? "✅ Yes" : "❌ No"} />
                <div style={{ marginTop:"12px", padding:"12px", background:"#0f172a", borderRadius:"8px" }}>
                  <p style={{ color:"#ec4899", fontSize:"12px", margin:"0 0 4px" }}>📝 Your Caption:</p>
                  <p style={{ color:"#f1f5f9", fontSize:"13px", margin:0 }}>
                    {cd?.original_caption || "No caption provided"}
                  </p>
                </div>
              </Card>

              <Card title="Person / Celebrity" icon="👤" accent="#8b5cf6">
                {cb?.celebrity_detected ? (
                  <div style={{ textAlign:"center", padding:"16px" }}>
                    <div style={{ fontSize:"48px", marginBottom:"8px" }}>🌟</div>
                    <p style={{ color:"#8b5cf6", fontSize:"20px", fontWeight:700, margin:0 }}>
                      {cb.celebrity_name}
                    </p>
                    <p style={{ color:"#64748b", fontSize:"13px" }}>Confidence: {cb.confidence}%</p>
                    <ScoreBar label="Match Score" value={cb.confidence} color="#8b5cf6" />
                  </div>
                ) : (
                  <div>
                    <p style={{ color:"#64748b", fontSize:"13px" }}>
                      👤 No celebrity match found in database
                    </p>
                    {vd?.detected_objects?.includes("person") && (
                      <p style={{ color:"#10b981", fontSize:"13px" }}>✅ Person detected in image</p>
                    )}
                    <p style={{ color:"#94a3b8", fontSize:"12px", marginTop:"8px" }}>
                      Tip: Add clear face images to your celebrities/ folder
                    </p>
                  </div>
                )}
                <div style={{ marginTop:"12px" }}>
                  <Row label="Has Person"      value={vd?.has_person ? "✅ Yes" : "❌ No"} />
                  <Row label="Engagement"      value={vd?.engagement_style} />
                  <Row label="All Categories"  value={vd?.all_categories} />
                </div>
              </Card>
            </div>
          )}

          {/* TAB: MUSIC */}
          {activeTab === "music" && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))", gap:"16px" }}>
              <Card title={`Regional Songs${stateInfo ? ` — ${stateInfo.name}` : ""}`} icon="🎵" accent="#a855f7">
                <p style={{ color:"#64748b", fontSize:"12px", margin:"0 0 10px" }}>
                  Trending {td?.category || "content"} songs in{" "}
                  {stateInfo ? stateInfo.name : country === "IN" ? "India" : country}:
                </p>
                {(td?.regional_songs?.length > 0 ? td.regional_songs : md?.recommended_songs || []).map((song,i) => (
                  <div key={i} style={{ display:"flex", alignItems:"center", gap:"10px",
                    padding:"8px 0", borderBottom:"1px solid #334155" }}>
                    <span style={{ color:"#a855f7", minWidth:"20px", textAlign:"center" }}>{i+1}</span>
                    <span style={{ color:"#f1f5f9", fontSize:"13px" }}>🎶 {song}</span>
                  </div>
                ))}
                {md?.song_details?.length > 0 && (
                  <div style={{ marginTop:"14px" }}>
                    <p style={{ color:"#a855f7", fontSize:"12px", margin:"0 0 8px" }}>▶️ YouTube Links:</p>
                    {md.song_details.slice(0,4).map((s,i) => (
                      <div key={i} style={{ marginBottom:"6px" }}>
                        <a href={s.url} target="_blank" rel="noreferrer"
                          style={{ color:"#c4b5fd", fontSize:"12px", textDecoration:"none" }}>
                          🎵 {s.title}
                        </a>
                        <span style={{ color:"#64748b", fontSize:"11px" }}> — {s.channel}</span>
                      </div>
                    ))}
                  </div>
                )}
              </Card>

              <Card title="Music Strategy" icon="🎬" accent="#06b6d4">
                <Row label="Visual Category" value={vd?.primary_category} />
                <Row label="Music Category"  value={md?.music_category} />
                <Row label="Reel Style"      value={md?.music_strategy?.best_reel_style} />
                <Row label="Best Platform"   value={md?.music_strategy?.recommended_platform} />
                <Row label="Viral Audio"     value={md?.music_strategy?.viral_audio_probability} />
                <Row label="Source"          value={md?.source} />
                <div style={{ marginTop:"12px", padding:"12px", background:"#0f172a", borderRadius:"8px" }}>
                  <p style={{ color:"#06b6d4", fontSize:"12px", margin:"0 0 4px" }}>💡 Pro Tip:</p>
                  <p style={{ color:"#94a3b8", fontSize:"12px", margin:0 }}>
                    Use the top regional song + trending audio for maximum reach on{" "}
                    {platforms[0] === "instagram" ? "Instagram Reels" :
                     platforms[0] === "youtube" ? "YouTube Shorts" : platforms[0]}.
                  </p>
                </div>
              </Card>
            </div>
          )}

          {/* TAB: HASHTAGS */}
          {activeTab === "hashtags" && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))", gap:"16px" }}>
              <Card title="All Recommended Hashtags" icon="#️⃣" accent="#06b6d4">
                <div style={{ marginBottom:"12px" }}>
                  {(hd?.recommended_hashtags||[]).map((t,i) => <Tag key={i} text={t} color="#06b6d4" />)}
                </div>
                <Row label="Total Count"     value={hd?.hashtag_count} />
                <Row label="Best Count"      value={hd?.hashtag_strategy?.best_count} />
                <Row label="Best Mix"        value={hd?.hashtag_strategy?.best_mix} />
                <Row label="Algorithm Boost" value={hd?.hashtag_strategy?.algorithm_boost} />
              </Card>

              <Card title="Hashtag Tiers" icon="🎯" accent="#f59e0b">
                <div style={{ marginBottom:"12px" }}>
                  <p style={{ color:"#ef4444", fontSize:"12px", margin:"0 0 6px" }}>🔥 Viral Tags:</p>
                  {(hd?.viral_hashtags||[]).map((t,i) => <Tag key={i} text={t} color="#ef4444" />)}
                </div>
                <div style={{ marginBottom:"12px" }}>
                  <p style={{ color:"#10b981", fontSize:"12px", margin:"0 0 6px" }}>🎯 Niche Tags:</p>
                  {(hd?.niche_hashtags||[]).map((t,i) => <Tag key={i} text={t} color="#10b981" />)}
                </div>
                <div>
                  <p style={{ color:"#06b6d4", fontSize:"12px", margin:"0 0 6px" }}>🚀 Rising Tags:</p>
                  {(td?.instagram_rising_tags||[]).map((t,i) => <Tag key={i} text={t} color="#06b6d4" />)}
                </div>
              </Card>

              <Card title={`Regional Hashtags${stateInfo ? ` — ${stateInfo.name}` : ""}`} icon="🌍" accent="#10b981">
                <p style={{ color:"#64748b", fontSize:"12px", margin:"0 0 10px" }}>
                  {stateInfo ? `Hashtags for ${stateInfo.name}:` : "Region-specific hashtags:"}
                </p>
                {(td?.hashtags||[]).map((t,i) => <Tag key={i} text={t} color="#10b981" />)}
              </Card>
            </div>
          )}

          {/* TAB: PLATFORM */}
          {activeTab === "platform" && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))", gap:"16px" }}>
              <Card title="Platform Recommendation" icon="🏆" accent="#f59e0b">
                <div style={{ background:"#0f172a", borderRadius:"10px", padding:"16px",
                  textAlign:"center", marginBottom:"14px" }}>
                  <p style={{ color:"#64748b", fontSize:"12px", margin:0 }}>Best Platform</p>
                  <p style={{ color:"#f59e0b", fontSize:"24px", fontWeight:700, margin:"6px 0" }}>
                    {pd?.best_platform}
                  </p>
                  <Tag text={pd?.viral_level||""} color="#f59e0b" />
                </div>
                <Row label="Upload Time"   value={pd?.best_upload_time} />
                <Row label="Duration"      value={pd?.best_video_duration} />
                <Row label="Frequency"     value={pd?.recommended_posting_frequency} />
                <Row label="Style"         value={pd?.recommended_content_style} />
                <Row label="Algorithm Tip" value={pd?.algorithm_tip} />
                {pd?.secondary_platforms?.length > 0 && (
                  <div style={{ marginTop:"10px" }}>
                    <p style={{ color:"#94a3b8", fontSize:"12px", margin:"0 0 4px" }}>Also post on:</p>
                    {pd.secondary_platforms.map((p,i) => <Tag key={i} text={p} color="#94a3b8" />)}
                  </div>
                )}
              </Card>

              <Card title="Strategy Tips" icon="💡" accent="#8b5cf6">
                {(pd?.strategy_tips||[]).map((tip,i) => (
                  <div key={i} style={{ padding:"8px 10px", background:"#0f172a",
                    borderRadius:"8px", marginBottom:"6px" }}>
                    <p style={{ color:"#f1f5f9", fontSize:"13px", margin:0 }}>{i+1}. {tip}</p>
                  </div>
                ))}
              </Card>

              <Card title="Engagement Forecast" icon="📊" accent="#06b6d4">
                <ScoreBar label="Engagement Score" value={ed?.engagement_score||0} color="#06b6d4" />
                <Row label="Probability" value={ed?.engagement_probability} />
                <Row label="Reach"       value={ed?.estimated_reach} />
                <Row label="Best Factor" value={ed?.best_engagement_factor} />
                {ed?.score_breakdown && (
                  <div style={{ marginTop:"12px" }}>
                    <p style={{ color:"#64748b", fontSize:"12px", margin:"0 0 8px" }}>Score Breakdown:</p>
                    <ScoreBar label="Visual"  value={ed.score_breakdown.visual||0}  max={40} color="#06b6d4" />
                    <ScoreBar label="Trend"   value={ed.score_breakdown.trend||0}   max={25} color="#10b981" />
                    <ScoreBar label="Caption" value={ed.score_breakdown.caption||0} max={20} color="#8b5cf6" />
                    <ScoreBar label="Music"   value={ed.score_breakdown.music||0}   max={10} color="#f59e0b" />
                    <ScoreBar label="Bonus"   value={ed.score_breakdown.bonus||0}   max={5}  color="#ec4899" />
                  </div>
                )}
                {ed?.improvement_tips?.length > 0 && (
                  <div style={{ marginTop:"10px" }}>
                    <p style={{ color:"#f59e0b", fontSize:"12px", margin:"0 0 6px" }}>💡 Improve:</p>
                    {ed.improvement_tips.map((t,i) => (
                      <p key={i} style={{ color:"#94a3b8", fontSize:"12px", margin:"3px 0" }}>• {t}</p>
                    ))}
                  </div>
                )}
              </Card>
            </div>
          )}

          {/* TAB: REGION */}
          {activeTab === "region" && (
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))", gap:"16px" }}>
              <Card title="Region Analysis" icon="🌍" accent="#10b981">
                <Row label="Region"      value={rd?.region} />
                <Row label="Best Time"   value={rd?.best_upload_time} />
                <Row label="Best Days"   value={rd?.best_days} />
                <Row label="Avg Watch"   value={rd?.avg_watch_time} />
                <Row label="Top Categories" value={rd?.top_categories} />
                <ScoreBar label="Regional Viral Score" value={rd?.regional_viral_score||0} color="#10b981" />
                <ScoreBar label="Audience Match"       value={rd?.audience_match_score||0} color="#06b6d4" />
              </Card>

              <Card title="Audience Profile" icon="👥" accent="#8b5cf6">
                <Row label="Behavior"  value={rd?.audience_behavior} />
                <Row label="Platforms" value={rd?.platform_priority} />
                {stateInfo && (
                  <div style={{ marginTop:"12px", padding:"12px",
                    background:"#0f172a", borderRadius:"8px" }}>
                    <p style={{ color:"#8b5cf6", fontSize:"13px", margin:"0 0 6px", fontWeight:600 }}>
                      {stateInfo.flag} {stateInfo.name}
                    </p>
                    <p style={{ color:"#94a3b8", fontSize:"12px", margin:0 }}>
                      Regional content strategy applied for {stateInfo.name}
                    </p>
                  </div>
                )}
                {rd?.recommendation && (
                  <div style={{ marginTop:"10px", padding:"10px",
                    background:"#10b98111", borderRadius:"8px" }}>
                    <p style={{ color:"#10b981", fontSize:"12px", margin:0 }}>💡 {rd.recommendation}</p>
                  </div>
                )}
              </Card>
            </div>
          )}

          {/* TAB: CAPTIONS */}
          {activeTab === "captions" && (
            <Card title="AI Generated Captions" icon="🤖" accent="#8b5cf6">
              <pre style={{ whiteSpace:"pre-wrap", color:"#f1f5f9", fontSize:"14px",
                margin:0, lineHeight:"1.8", background:"#0f172a",
                padding:"20px", borderRadius:"10px" }}>
                {ac?.generated_caption || "No caption generated"}
              </pre>
            </Card>
          )}

          {/* TAB: REPORT */}
          {activeTab === "report" && (
            <Card title="Final AI Report" icon="📋" accent="#06b6d4">
              <div style={{ background:"#0f172a", padding:"20px", borderRadius:"10px",
                whiteSpace:"pre-wrap", fontSize:"13px", color:"#e2e8f0", lineHeight:"1.9" }}>
                {r?.final_report || "Final report unavailable"}
              </div>
            </Card>
          )}

        </div>
      )}
    </div>
  );
}
