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

LOGIN_HTML = """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#000;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh}.card{background:#111;border:1px solid #222;border-radius:24px;padding:40px;text-align:center;width:90%;max-width:400px}h1{font-size:40px;font-weight:900}h1 span{color:#a855f7}.btn{background:#fff;color:#000;padding:14px;border-radius:999px;text-decoration:none;font-weight:800;display:block;margin-top:20px}</style></head><body><div class="card"><h1>ClipViral<span>.AI</span> 🚀</h1><p style="color:#888;margin-top:8px">YouTube • TikTok • Twitch • Kick</p><a class="btn" href="/login/google">Continuar con Google</a></div></body></html>"""

DASH_HTML = """<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#000;color:#fff;font-family:sans-serif;padding:20px}.top{max-width:1000px;margin:0 auto;display:flex;justify-content:space-between;margin-bottom:20px}.main{max-width:1000px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:20px}@media(max-width:800px){.main{grid-template-columns:1fr}}.card{background:#111;border:1px solid #222;border-radius:18px;padding:20px}.input{width:100%;background:#18181b;border:1px solid #333;border-radius:10px;padding:12px;color:#fff}.btn-w{background:#fff;color:#000;padding:12px;border-radius:999px;font-weight:800;border:none;width:100%;margin-top:12px;cursor:pointer}.clip{background:#18181b;border:1px solid #27272a;border-radius:10px;padding:12px;margin-bottom:8px;display:flex;justify-content:space-between}</style></head><body><div class="top"><div style="font-weight:900">ClipViral<span style="color:#a855f7">.AI</span></div><div style="color:#888;font-size:12px">{{email}} | <a href="/logout" style="color:#fff">Salir</a></div></div><div class="main"><div class="card"><h2>Pega link 🔗</h2><form action="/analyze" method="post"><input class="input" type="text" name="video_url" placeholder="youtube.com / tiktok.com / twitch.tv / kick.com"><button class="btn-w" type="submit">Analizar con IA</button></form>{% if source %}<div style="margin-top:10px;background:#222;padding:5px 10px;border-radius:20px;font-size:11px;display:inline-block">{{source}}</div>{% endif %}</div><div class="card"><h2>Clips 🔥</h2>{% if clips %}{% for c in clips %}<div class="clip"><div><b>{{c.score}}/100</b><br><span style="color:#888;font-size:11px">{{c.reason}}</span><br><span style="font-size:12px">{{c.hook}}</span></div></div>{% endfor %}{% else %}<div style="color:#555;text-align:center;padding:30px">Pega un link arriba</div>{% endif %}</div></div></body></html>"""

def detect(u):
    if not u: return "Local"
    u=u.lower()
    if "youtu" in u: return "YouTube"
    if "tiktok" in u: return "TikTok"
    if "twitch" in u: return "Twitch"
    if "kick" in u: return "Kick"
    return "Link"

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
    url = request.form.get('video_url','')
    time.sleep(1)
    clips=[]
    for i in range(5):
        clips.append({"score":random.randint(88,99),"reason":random.choice(["Hook viral","Pico energia"]),"hook":random.choice(["Nadie te dice esto","El secreto"])})
    session['clips']=clips
    session['source']=detect(url)+" - "+url[:35]
    return redirect('/dashboard')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
