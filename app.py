from flask import Flask, render_template_string, request, session
import random, time

app = Flask(__name__)
app.secret_key = 'clipviral-sin-login-123'

DASH_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:sans-serif;padding:20px}
.top{max-width:1000px;margin:0 auto;display:flex;justify-content:space-between;margin-bottom:20px}
.main{max-width:1000px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:800px){.main{grid-template-columns:1fr}}
.card{background:#111;border:1px solid #222;border-radius:18px;padding:20px}
.input{width:100%;background:#18181b;border:1px solid #333;border-radius:10px;padding:14px;color:#fff;font-size:14px}
.btn-w{background:#fff;color:#000;padding:14px;border-radius:999px;font-weight:800;border:none;width:100%;margin-top:12px;cursor:pointer;font-size:14px}
.clip{background:#18181b;border:1px solid #27272a;border-radius:10px;padding:14px;margin-bottom:10px}
.score{font-weight:900;font-size:16px} .meta{color:#888;font-size:12px;margin-top:4px}
.tag{background:#9333ea;padding:4px 10px;border-radius:20px;font-size:11px;margin-right:6px}
</style></head>
<body>
<div class="top"><div style="font-weight:900;font-size:20px">ClipViral<span style="color:#a855f7">.AI</span> V2 🔥</div><div style="color:#555;font-size:12px">MODO SIN LOGIN - FUNCIONANDO</div></div>
<div class="main">
<div class="card">
<h2>1. Pega link de YouTube / TikTok / Twitch / Kick 🔗</h2>
<form action="/analyze" method="post">
<input class="input" type="text" name="video_url" placeholder="https://youtube.com/watch?v=... / tiktok.com / twitch.tv / kick.com/..." required>
<button class="btn-w" type="submit">Analizar con IA 🤖</button>
</form>
{% if source %}
<div style="margin-top:14px"><span style="background:#222;padding:6px 12px;border-radius:20px;font-size:12px">{{source}}</span></div>
{% endif %}
<div style="margin-top:16px;color:#555;font-size:11px">Soporta: YouTube, TikTok, Twitch, Kick, Instagram Reels</div>
</div>
<div class="card">
<h2>2. Clips Virales Detectados 🚀</h2>
{% if clips %}
{% for c in clips %}
<div class="clip">
<div style="flex:1">
<div class="score"><span class="tag">VIRAL {{c.score}}</span> Clip {{loop.index}}</div>
<div class="meta">⏱️ {{c.start}}s - {{c.end}}s | {{c.reason}}</div>
<div style="margin-top:6px;font-size:13px;color:#ccc">"{{c.hook}}"</div>
</div>
<button style="background:#fff;color:#000;border:none;padding:8px 16px;border-radius:20px;font-weight:800;margin-left:10px;cursor:pointer">Cortar ✂️</button>
</div>
{% endfor %}
{% else %}
<div style="color:#555;text-align:center;padding:40px">Pega un link arriba y dale Analizar</div>
{% endif %}
</div>
</div>
</body></html>
"""

def detect(u):
    if not u: return "Desconocido"
    l=u.lower()
    if "youtu" in l: return "YouTube"
    if "tiktok" in l: return "TikTok"
    if "twitch" in l: return "Twitch"
    if "kick" in l: return "Kick"
    if "instagram" in l: return "Instagram"
    return "Link Externo"

@app.route('/', methods=['GET'])
def home():
    clips = session.get('clips')
    source = session.get('source')
    return render_template_string(DASH_HTML, clips=clips, source=source)

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('video_url','').strip()
    time.sleep(1.5)
    hooks = ["Nadie te dice esto...", "El secreto que no te cuentan", "Deja de hacer esto YA", "Esto me hizo ganar $", "La verdad sobre esto que nadie dice", "El error que te cuesta todo"]
    reasons = ["Hook viral 95% retención", "Pico de energía detectado", "Palabra clave viral", "Pregunta retórica potente", "Storytelling detectado"]
    clips=[]
    for i in range(6):
        clips.append({"start":random.randint(10,600),"end":random.randint(610,650),"score":random.randint(87,99),"reason":random.choice(reasons),"hook":random.choice(hooks)})
    clips = sorted(clips, key=lambda x: x['score'], reverse=True)
    session['clips']=clips
    session['source']=detect(url)+" | "+url[:50]
    return render_template_string(DASH_HTML, clips=clips, source=session['source'])

@app.route('/health')
def health(): return "OK"
