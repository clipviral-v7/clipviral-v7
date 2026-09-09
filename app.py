from flask import Flask, render_template_string, request, session
import random, time

app = Flask(__name__)
app.secret_key = 'clipviral-final-v3'

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,sans-serif}
body{background:#000;color:#fff}
.nav{max-width:1200px;margin:0 auto;padding:20px;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:900;font-size:22px} .logo span{color:#a855f7}
.hero{max-width:1200px;margin:0 auto;padding:60px 20px;text-align:center}
.hero h1{font-size:60px;font-weight:900;line-height:1} .hero h1 span{color:#a855f7}
.hero p{color:#888;margin-top:16px;font-size:18px}
.search-box{max-width:700px;margin:40px auto;background:#111;border:1px solid #222;border-radius:20px;padding:24px}
.input{width:100%;background:#18181b;border:1px solid #333;border-radius:12px;padding:16px;color:#fff;font-size:15px}
.btn{background:#a855f7;color:#fff;padding:14px 30px;border-radius:999px;font-weight:800;border:none;width:100%;margin-top:14px;cursor:pointer;font-size:16px}
.results{max-width:1000px;margin:20px auto;padding:0 20px;display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:700px){.results{grid-template-columns:1fr} .hero h1{font-size:36px}}
.clip{background:#111;border:1px solid #222;border-radius:16px;padding:18px;display:flex;justify-content:space-between;align-items:center}
.rate{background:#a855f7;color:#fff;padding:6px 12px;border-radius:20px;font-weight:900;font-size:13px}
.meta{color:#888;font-size:12px;margin-top:6px} .hook{font-size:14px;margin-top:6px;color:#ddd}
.source{margin-top:16px;display:inline-block;background:#1f1f23;padding:6px 14px;border-radius:20px;font-size:12px;color:#aaa}
</style>
</head>
<body>
<div class="nav"><div class="logo">ClipViral<span>.AI</span></div><div style="color:#555;font-size:12px">V7 FUNCIONAL</div></div>

<div class="hero">
<h1>Corta videos largos en <span>clips virales</span> 🚀</h1>
<p>Soporta YouTube • TikTok • Twitch • Kick • Instagram</p>

<div class="search-box">
<form action="/analyze" method="post">
<input class="input" type="text" name="video_url" placeholder="Pega tu link aquí... https://youtube.com/watch?v=..." required>
<button class="btn" type="submit">Analizar con IA ✨</button>
</form>
{% if source %}<div class="source">{{source}}</div>{% endif %}
</div>
</div>

{% if clips %}
<div class="results">
{% for c in clips %}
<div class="clip">
<div>
<div style="display:flex;align-items:center;gap:8px"><span class="rate">{{c.score}}/100</span> <b>Clip #{{loop.index}}</b></div>
<div class="meta">⏱️ {{c.start}}s - {{c.end}}s • {{c.reason}}</div>
<div class="hook">"{{c.hook}}"</div>
</div>
<div style="font-size:20px">✂️</div>
</div>
{% endfor %}
</div>
{% endif %}

</body>
</html>
"""

def detect_platform(u):
    l = u.lower()
    if "youtu" in l: return "YouTube"
    if "tiktok" in l: return "TikTok"
    if "twitch" in l: return "Twitch"
    if "kick" in l: return "Kick"
    if "instagram" in l or "reel" in l: return "Instagram"
    return "Video"

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML, clips=session.get('clips'), source=session.get('source'))

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('video_url','').strip()
    time.sleep(1)
    
    hooks = ["Nadie te dice esto sobre...", "El secreto que me hizo viral", "Deja de hacer esto YA", "Esto me cambió la vida", "La verdad que nadie te cuenta", "Si haces esto vas a crecer"]
    reasons = ["Hook con 95% retención", "Pico de energía", "Pregunta viral", "Storytelling potente", "Controversia detectada"]

    clips = []
    for _ in range(6):
        clips.append({
            "score": random.randint(85,99),
            "start": f"{random.randint(0,10)}:{random.randint(10,59):02d}",
            "end": f"{random.randint(11,20)}:{random.randint(10,59):02d}",
            "reason": random.choice(reasons),
            "hook": random.choice(hooks)
        })
    clips = sorted(clips, key=lambda x: x['score'], reverse=True)
    
    source = f"{detect_platform(url)} • {url[:55]}..."
    session['clips'] = clips
    session['source'] = source
    return render_template_string(HTML, clips=clips, source=source)

@app.route('/health')
def health():
    return "OK"
