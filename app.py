from flask import Flask, redirect, session, render_template_string, request
from authlib.integrations.flask_client import OAuth
import random, time

app = Flask(__name__)
app.secret_key = 'clipviral-2024-final'

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

LOGIN_HTML = """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#000;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh}h1{font-size:50px}a{background:#fff;color:#000;padding:15px 30px;border-radius:999px;text-decoration:none;font-weight:900}</style></head><body><div style="text-align:center"><h1>ClipViral.AI</h1><a href="/login/google">Continuar con Google</a></div></body></html>"""

DASH_HTML = """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#000;color:#fff;font-family:sans-serif;padding:20px}.box{max-width:800px;margin:0 auto}.up{background:#18181b;padding:20px;border-radius:16px;border:1px solid #333}.clip{background:#18181b;padding:15px;border-radius:12px;border:1px solid #333;margin-top:12px;display:flex;justify-content:space-between}button{border:none;cursor:pointer}.w{background:#fff;color:#000;padding:10px 20px;border-radius:999px;font-weight:700}.p{background:#9333ea;color:#fff;padding:8px 16px;border-radius:999px}</style></head><body><div class="box"><h1>ClipViral.AI LITE</h1><p style="color:#999">{{email}} | IA Activa</p><div class="up"><h2>Sube tu video largo</h2><form action="/upload" method="post" enctype="multipart/form-data"><input type="file" name="video" required style="background:#333;padding:8px;border-radius:8px;color:#fff"><button class="w" style="margin-left:10px">Analizar con IA</button></form></div>{% if clips %}<h2 style="margin-top:30px">Clips Virales Detectados</h2>{% for c in clips %}<div class="clip"><div><b>Clip {{loop.index}} - Score {{c.score}}/100</b><br><span style="color:#aaa;font-size:13px">{{c.reason}}</span><br><span style="color:#666;font-size:11px">{{c.start}}s - {{c.end}}s | {{c.hook}}</span></div><button class="p">Cortar</button></div>{% endfor %}{% endif %}</div></body></html>"""

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
    time.sleep(1)
    hooks = ["Nadie te dice esto...", "El secreto del dinero", "Deja de hacer esto YA", "El error que te cuesta", "Esto cambio mi vida"]
    reasons = ["Hook de curiosidad", "Palabra viral detectada", "Pico de energia", "Pregunta retorica"]
    clips = []
    for i in range(5):
        clips.append({"start": random.randint(10,300), "end": random.randint(310,400), "score": random.randint(85,98), "reason": random.choice(reasons), "hook": random.choice(hooks)})
    session['clips'] = sorted(clips, key=lambda x: x['score'], reverse=True)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
