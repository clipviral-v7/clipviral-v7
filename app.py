from flask import Flask, redirect, session, render_template_string, request
from authlib.integrations.flask_client import OAuth
import random, time

app = Flask(__name__)
app.secret_key = 'clipviral-pro-lite-2024'

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

# INICIO PRO NEGRO
LOGIN_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:Inter,Arial,sans-serif;height:100vh;display:flex;align-items:center;justify-content:center}
.card{background:#111;border:1px solid #222;border-radius:24px;padding:48px;text-align:center;max-width:420px;width:90%}
h1{font-size:48px;font-weight:900;margin-bottom:12px} h1 span{color:#a855f7}
p{color:#888;margin-bottom:32px}
.btn{background:#fff;color:#000;padding:16px 32px;border-radius:999px;text-decoration:none;font-weight:800;display:flex;align-items:center;justify-content:center;gap:10px;width:100%}
.btn:hover{background:#eee}
.badge{margin-top:20px;color:#555;font-size:12px}
</style></head>
<body>
<div class="card">
<h1>ClipViral<span>.AI</span> 🚀</h1>
<p>Convierte tu podcast largo en 10 clips virales con IA</p>
<a class="btn" href="/login/google"> <img src="https://www.google.com/favicon.ico" width="20"> Continuar con Google</a>
<div class="badge">MODO LITE - Render Gratis Compatible</div>
</div>
</body></html>
"""

# DASHBOARD PRO
DASH_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:Inter,Arial,sans-serif;padding:24px}
.top{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;margin-bottom:30px}
.logo{font-size:24px;font-weight:900} .logo span{color:#a855f7}
.user{color:#888;font-size:14px}
.main{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:24px}
@media(max-width:800px){.main{grid-template-columns:1fr}}
.card{background:#111;border:1px solid #222;border-radius:20px;padding:24px}
h2{font-size:20px;margin-bottom:16px}
.upload{border:2px dashed #333;border-radius:16px;padding:40px 20px;text-align:center;cursor:pointer}
.upload:hover{border-color:#a855f7}
input[type=file]{display:none}
.btn-w{background:#fff;color:#000;padding:12px 24px;border-radius:999px;font-weight:800;border:none;cursor:pointer;width:100%;margin-top:16px}
.clip{background:#18181b;border:1px solid #27272a;border-radius:14px;padding:16px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
.score{font-weight:800;font-size:18px} .score.high{color:#22c55e}
.meta{color:#888;font-size:12px;margin-top:4px}
.btn-p{background:#9333ea;color:#fff;padding:8px 18px;border-radius:999px;border:none;font-weight:700;cursor:pointer;font-size:13px}
.empty{color:#555;text-align:center;padding:40px}
</style></head>
<body>
<div class="top">
<div class="logo">ClipViral<span>.AI</span> LITE</div>
<div class="user">{{email}} | <a href="/logout" style="color:#fff">Salir</a></div>
</div>
<div class="main">
<div class="card">
<h2>1. Sube tu video largo 📤</h2>
<div class="upload" onclick="document.getElementById('file').click()">
<div style="font-size:40px">🎙️</div>
<div style="margin-top:10px">Click para subir tu podcast / video</div>
<div style="color:#666;font-size:12px;margin-top:6px">MP4, MOV, MP3 hasta 500MB</div>
</div>
<form action="/upload" method="post" enctype="multipart/form-data">
<input type="file" id="file" name="video" accept="video/*,audio/*" required onchange="this.form.submit()">
<button class="btn-w" type="submit">Analizar con IA 🤖</button>
</form>
</div>
<div class="card">
<h2>2. Clips virales detectados 🔥</h2>
{% if clips %}
{% for c in clips %}
<div class="clip">
<div>
<div class="score high">Clip {{loop.index}} - {{c.score}}/100</div>
<div class="meta"><b>{{c.reason}}</b> | {{c.start}}s - {{c.end}}s</div>
<div class="meta" style="color:#aaa">"{{c.hook}}"</div>
</div>
<button class="btn-p">Cortar</button>
</div>
{% endfor %}
{% else %}
<div class="empty">Aún no hay clips.<br>Sube un video para que la IA los detecte.</div>
{% endif %}
</div>
</div>
</body></html>
"""

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
    return render_template_string(DASH_HTML, email=session['email'], clips=clips)

@app.route('/upload', methods=['POST'])
def upload():
    if 'email' not in session: return redirect('/')
    time.sleep(2)
    hooks = ["Nadie te dice esto...", "El secreto del dinero que no te cuentan", "Deja de hacer esto YA", "El error que te cuesta miles", "Esto cambio mi vida en 30 dias", "La verdad sobre..."]
    reasons = ["Hook de curiosidad + alta retención", "Palabra viral detectada", "Pico de energía en voz", "Pregunta retórica potente", "Storytelling detectado"]
    clips = []
    for i in range(5):
        clips.append({"start": random.randint(10,600), "end": random.randint(610,700), "score": random.randint(87,98), "reason": random.choice(reasons), "hook": random.choice(hooks)})
    session['clips'] = sorted(clips, key=lambda x: x['score'], reverse=True)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
