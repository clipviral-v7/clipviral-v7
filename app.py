import os, random, time
from flask import Flask, redirect, url_for, session, render_template_string, request
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'clipviral-super-secret-2024'

GOOGLE_CLIENT_ID = '279980196781-9qsd701ujr47rbj84a1k88sseps9rdtd.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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3' # TU MISMO SECRET

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

DASHBOARD_HTML = """
<!DOCTYPE html><html><head><title>ClipViral.AI</title>
<script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-black text-white p-8">
<div class="max-w-4xl mx-auto">
<h1 class="text-4xl font-bold mb-2">ClipViral.AI 🚀 LITE</h1>
<p class="text-zinc-400 mb-8">Logueado: {{email}} | IA Activa</p>
<div class="bg-zinc-900 p-6 rounded-2xl border border-zinc-800">
<h2 class="text-2xl font-bold mb-4">1. Sube tu Podcast / Video largo</h2>
<form action="/upload" method="post" enctype="multipart/form-data" class="flex gap-4">
<input type="file" name="video" accept="video/*" class="bg-zinc-800 p-2 rounded w-full" required>
<button class="bg-white text-black px-6 py-2 rounded-full font-bold">Analizar con IA</button>
</form>
<p class="text-xs text-zinc-500 mt-2">*Analizamos con IA de texto + energía de audio (versión nube)</p>
</div>
{% if clips %}
<div class="mt-10">
<h2 class="text-2xl font-bold mb-4">🔥 Clips Virales Detectados</h2>
<div class="grid grid-cols-1 gap-4">
{% for clip in clips %}
<div class="bg-zinc-900 p-4 rounded-xl border border-zinc-800 flex justify-between items-center">
<div><p class="font-bold text-lg">Clip {{loop.index}} - Viral Score: {{clip.score}}/100</p>
<p class="text-zinc-400 text-sm">{{clip.reason}}</p><p class="text-zinc-500 text-xs mt-1">{{clip.start}}s - {{clip.end}}s | Hook: "{{clip.hook}}"</p></div>
<button class="bg-purple-600 px-4 py-2 rounded-full text-sm">Cortar Clip</button></div>
{% endfor %}
</div></div>
{% endif %}
</div></body></html>
"""
LOGIN_HTML = """<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-black text-white flex h-screen items-center justify-center"><div class="text-center">
<h1 class="text-5xl font-bold mb-8">ClipViral.AI</h1><a href="/login/google" class="bg-white text-black px-8 py-3 rounded-full font-bold">Continuar con Google</a></div></body></html>"""

@app.route('/')
def home(): return render_template_string(LOGIN_HTML)
@app.route('/login')
def login_page(): return render_template_string(LOGIN_HTML)
@app.route('/login/google')
def login_google(): return google.authorize_redirect(url_for('auth_callback', _external=True))
@app.route('/auth/google/callback')
def auth_callback():
    token = google.authorize_access_token()
    user = token.get('userinfo')
    session['email'] = user['email']
    return redirect('/dashboard')
@app.route('/dashboard')
def dashboard():
    if 'email' not in session: return redirect('/login')
    clips = session.pop('clips', None)
    return render_template_string(DASHBOARD_HTML, email=session['email'], clips=clips)
@app.route('/upload', methods=['POST'])
def upload():
    if 'email' not in session: return redirect('/login')
    time.sleep(2) # Simula analisis de IA
    hooks = ["Nadie te dice esto...", "El error que te cuesta dinero", "El secreto que ocultan", "Esto cambió mi vida", "Deja de hacer esto YA"]
    reasons = ["Hook de curiosidad + retención alta", "Contiene palabra viral 'dinero/secreto'", "Pico de energía en audio detectado", "Pregunta retórica + loop abierto", "Storytelling con tensión"]
    clips = []
    for i in range(5):
        clips.append({"start": random.randint(10, 500), "end": random.randint(510, 800), "score": random.randint(82, 98), "reason": random.choice(reasons), "hook": random.choice(hooks)})
    session['clips'] = sorted(clips, key=lambda x: x['score'], reverse=True)
    return redirect('/dashboard')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
