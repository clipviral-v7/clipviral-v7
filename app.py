from flask import Flask, redirect, session, render_template_string, request
from authlib.integrations.flask_client import OAuth
import random, time, re

app = Flask(__name__)
app.secret_key = 'clipviral-v2-links'

GOOGLE_CLIENT_ID = '279980196781-9qsd701ujr47rbj84a1k88sseps9rdtd.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

LOGIN_HTML = """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#000;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh}.card{background:#111;border:1px solid #222;border-radius:24px;padding:48px;text-align:center;max-width:420px;width:90%}h1{font-size:44px;font-weight:900;margin-bottom:10px}h1 span{color:#a855f7}p{color:#888;margin-bottom:30px}.btn{background:#fff;color:#000;padding:16px 32px;border-radius:999px;text-decoration:none;font-weight:800;display:block;width:100%}</style></head><body><div class="card"><h1>ClipViral<span>.AI</span> 🚀</h1><p>De YouTube, TikTok, Twitch, Kick a clips virales</p><a class="btn" href="/login/google">Continuar con Google</a></div></body></html>"""

DASH_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:sans-serif;padding:20px}
.top{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;margin-bottom:28px}
.logo{font-size:22px;font-weight:900}.logo span{color:#a855f7}
.main{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:800px){.main{grid-template-columns:1fr}}
.card{background:#111;border:1px solid #222;border-radius:20px;padding:24px}
h2{font-size:18px;margin-bottom:14px}
.input{width:100%;background:#18181b;border:1px solid #333;border-radius:12px;padding:14px;color:#fff;margin-bottom:12px}
.btn-w{background:#fff;color:#000;padding:12px;border-radius:999px;font-weight:800;border:none;cursor:pointer;width:100%}
.or{text-align:center;color:#555;margin:14px 0;font-size:13px}
.clip{background:#18181b;border:1px solid #27272a;border-radius:12px;padding:14px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
.score{font-weight:800}.meta{color:#888;font-size:11px;margin-top:3px}
.btn-p{background:#9333ea;color:#fff;padding:8px 16px;border-radius:999px;border:none;font-weight:700;cursor:pointer;font-size:12px}
.source{background:#222;padding:6px 10px;border-radius:999px;font-size:11px;color:#aaa;margin-bottom:12px;display:inline-block}
</style></head>
<body>
<div class="top"><div class="logo">ClipViral<span>.AI</span> V2</div><div style="color:#888;font-size:13px">{{email}} | <a href="/logout" style="color:#fff">Salir</a></div></div>
<div class="main">
<div class="card">
<h2>1. Pega link o sube video 🔗</h2>
<form action="/analyze" method="post" enctype="multipart/form-data">
<input class="input" type="url" name="video_url" placeholder="https://youtube.com/watch?v=... / tiktok.com / twitch.tv / kick.com/...">
<div class="or">— o —</div>
<input type="file" name="video" accept="video/*,audio/*" style="background:#18181b;padding:10px;border-radius:10px;border:1px dashed #333;width:100%;color:#888">
<button class="btn-w" type="submit" style="margin-top:14px">Analizar con IA 🤖</button>
<p style="color:#555;font-size:11px;margin-top:10px;text-align:center">Soporta YouTube, TikTok, Twitch, Kick, Instagram</p>
</form>
{% if source %}<div style="margin-top:16px"><span class="source">Fuente: {{source}}</span></div>{% endif %}
</div>
<div class="card">
<h2>2. Clips virales 🔥</h2>
{% if clips %}
{% for c in clips %}<div class="clip"><div><div class="score">Clip {{loop.index}} - {{c.score}}/100 🔥</div><div class="meta">{{c.reason}} | {{c.start}}s-{{c.end}}s</div><div class="meta" style="color:#ccc">"{{c.hook}}"</div></div><button class="btn-p">Cortar</button></div>{% endfor %}
{% else %}<div style="color:#555;text-align:center;padding:40px">Pega un link arriba para empezar</div>{% endif %}
</div>
</div>
</body></html>
"""

def detect_platform(url):
    if not url: return "Archivo local"
    if "youtube.com" in url or "youtu.be" in url: return "YouTube"
    if "tiktok.com" in url: return "TikTok"
    if "twitch.tv" in url: return "Twitch"
    if "kick.com" in url: return "Kick"
    if "instagram.com" in url: return "Instagram"
    return "Link externo"

@app.route('/')
def home(): return render_template_string(LOGIN_HTML)
@app.route('/login/google')
def login_google(): return google.authorize_redirect('https://clipviral-v7.onrender.com/auth/google/callback')
@app.route('/auth/google/callback')
def auth_callback():
    token = google.authorize_access_token()
    user = token.get('userinfo')
    if user: session['email'] = user['email']
    return redirect('/dashboard')
@app.route('/dashboard')
def dashboard():
    if 'email' not in session: return redirect('/')
    clips = session.pop('clips', None)
    source = session.pop('source', None)
    return render_template_string(DASH_HTML, email=session['email'], clips=clips, source=source)
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'email' not in session: return redirect('/')
    url = request.form.get('video_url','').strip()
    source = detect_platform(url)
    # Aqui luego usamos yt-dlp para descargar info real, por ahora es MOCK LITE
    time.sleep(2)
    hooks = ["Nadie te dice esto...", "El secreto que no te cuentan", "Deja de hacer esto YA", "Esto me hizo ganar", "La verdad sobre esto"]
    reasons = ["Hook viral 95% retención", "Palabra clave viral", "Pico de energía detectado", "Pregunta retórica"]
    clips = []
    for i in range(6):
        clips.append({"start": random.randint(5,500), "end": random.randint(510,600), "score": random.randint(88,99), "reason": random.choice(reasons), "hook": random.choice(hooks)})
    session['clips'] = sorted(clips, key=lambda x: x['score'], reverse=True)
    session['source'] = source + (f" - {url[:40]}..." if url else "")
    return redirect('/dashboard')
@app.route('/upload', methods=['POST'])
def upload(): return redirect('/dashboard')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
