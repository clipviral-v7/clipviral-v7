from flask import Flask, request
import random

app = Flask(__name__)

# ---------- HOME ----------
HOME_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipViral.AI</title>
<style>
body{margin:0;background:#000;color:#fff;font-family:Inter,sans-serif}
.nav{padding:20px 30px;display:flex;justify-content:space-between;align-items:center;max-width:1200px;margin:0 auto}
.logo{font-weight:900;font-size:22px}.logo span{color:#a855f7}
.nav a{background:#a855f7;color:#fff;padding:8px 18px;border-radius:20px;text-decoration:none;font-weight:800;font-size:13px}
.hero{text-align:center;padding:60px 20px}
h1{font-size:52px;font-weight:900;line-height:1.05;margin:0} h1 span{color:#a855f7}
.sub{color:#888;margin-top:12px;font-size:16px}
.box{max-width:650px;margin:30px auto;background:#111;border:1px solid #222;border-radius:20px;padding:24px}
input{width:100%;padding:16px;border-radius:12px;background:#18181b;border:1px solid #333;color:#fff;font-size:14px;box-sizing:border-box}
button{width:100%;margin-top:12px;padding:14px;border-radius:999px;background:#a855f7;color:#fff;font-weight:800;border:none;font-size:16px;cursor:pointer}
.platforms{color:#555;font-size:11px;margin-top:10px;text-align:center}
.features{display:flex;gap:14px;max-width:900px;margin:40px auto;padding:0 20px;flex-wrap:wrap;justify-content:center}
.feat{background:#111;border:1px solid #1a1a1a;border-radius:14px;padding:16px;width:220px;text-align:left}
.rate{color:#a855f7;font-weight:900}
</style></head><body>
<div class="nav"><div class="logo">ClipViral<span>.AI</span></div><a href="/dashboard">Dashboard →</a></div>
<div class="hero">
<h1>Corta videos largos en<br><span>clips virales</span> 🚀</h1>
<p class="sub">IA que analiza tus directos y te dice que clips pueden ser virales con score 92%+</p>
<div class="box">
<form method="post" action="/dashboard">
<input name="url" placeholder="Pega link: youtube.com / kick.com/westcol / twitch.tv..." required>
<button type="submit">Analizar con IA ✨</button>
<div class="platforms">Soporta YouTube • Kick • Twitch • Upload local</div>
</form>
</div>
<div class="features">
<div class="feat"><div class="rate">92% Viral Score</div><div style="font-size:13px;margin-top:6px;color:#aaa">Te dice el % de viralidad de cada clip</div></div>
<div class="feat"><div class="rate">Hook Titles</div><div style="font-size:13px;margin-top:6px;color:#aaa">Te genera títulos virales automáticos</div></div>
<div class="feat"><div class="rate">Auto Subtítulos</div><div style="font-size:13px;margin-top:6px;color:#aaa">Amarillo neón, morado, el color que quieras</div></div>
</div>
<p style="text-align:center;margin-top:30px"><a href="/dashboard" style="color:#a855f7;text-decoration:none;font-weight:800">→ Ir al Dashboard PRO como la captura</a></p>
</div></body></html>
"""

# ---------- DASHBOARD COMO CAPTURA ----------
DASH_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipGenius - Dashboard</title>
<style>
body{margin:0;background:#0a0a0a;color:#fff;font-family:Inter,sans-serif}
.top{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;background:#111;border-bottom:1px solid #1e1e1e}
.logo{font-weight:900} .logo span{color:#a855f7} .logo small{color:#666;font-weight:400;font-size:10px;display:block}
.menu{display:flex;gap:18px;color:#666;font-size:12px} .menu b{color:#fff}
.wrap{display:flex;gap:16px;padding:16px;max-width:1400px;margin:0 auto;flex-wrap:wrap}
.left{flex:1;min-width:320px;background:#121212;border:1px solid #1e1e1e;border-radius:16px;padding:16px}
.right{flex:1.2;min-width:340px;background:#121212;border:1px solid #1e1e1e;border-radius:16px;padding:16px}
.box-title{font-size:12px;font-weight:800;color:#aaa;margin-bottom:10px;letter-spacing:0.5px}
.upload{border:1.5px dashed #2a2a2a;border-radius:12px;padding:28px;text-align:center;background:#0f0f0f}
.upload b{color:#fff;font-size:13px}
.upload p{color:#555;font-size:11px;margin:6px 0 0}
.urlbox{margin-top:14px}
.urlbox input{width:100%;padding:12px;border-radius:10px;background:#0a0a0a;border:1px solid #222;color:#fff;font-size:12px;box-sizing:border-box}
.colors{display:flex;gap:8px;margin-top:10px}
.dot{width:22px;height:22px;border-radius:50%;cursor:pointer;border:2px solid #000}
.preview{aspect-ratio:16/9;background:#000;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#555;font-size:12px;position:relative;overflow:hidden;border:1px solid #222}
.score-box{display:flex;gap:16px;margin-top:14px}
.circle{width:90px;height:90px;border-radius:50%;background:radial-gradient(circle at center,#1a1a1a 60%,#a855f7 61%);display:flex;flex-direction:column;align-items:center;justify-content:center}
.circle b{font-size:22px;color:#a855f7} .circle span{font-size:8px;color:#888}
.hooks{flex:1}
.hook{background:#0f0f0f;border:1px solid #1e1e1e;border-radius:10px;padding:8px 10px;margin-bottom:6px;display:flex;justify-content:space-between;font-size:11px}
.hook span:last-child{color:#a855f7;font-weight:800}
.btn{display:block;width:100%;margin-top:16px;padding:14px;border-radius:12px;background:#a855f7;color:#fff;font-weight:900;border:none;text-align:center;font-size:14px;cursor:pointer}
.clips{max-width:1400px;margin:0 auto;padding:0 16px 30px;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.clip-card{background:#121212;border:1px solid #1e1e1e;border-radius:14px;padding:12px}
</style></head><body>
<div class="top">
<div class="logo">💜 ClipGenius <span style="color:#a855f7">AI Video Clipper</span><small>Gradia v4.30 • Dashboard</small></div>
<div class="menu"><b>Dashboard</b><span>Library</span><span>Analytics</span><span>Settings</span></div>
</div>

<div class="wrap">
<div class="left">
<div class="box-title">⬆️ UPLOAD VIDEO</div>
<div class="upload">
<b>Drag & drop your video here</b>
<p>MP4, MOV, AVI, WEBM up to 2GB • or paste URL below</p>
<p style="margin-top:10px">📁 Click to browse files</p>
</div>
<div class="urlbox">
<div class="box-title">🔗 O PEGA URL (YouTube / Kick / Twitch)</div>
<form method="post" action="/dashboard">
<input name="url" placeholder="https://youtube.com/watch?v=... o kick.com/westcol/videos/..." value="URL_VALUE">
<button type="submit" style="margin-top:8px;padding:10px;border-radius:10px;background:#222;color:#fff;border:none;width:100%;font-weight:700">Cargar URL →</button>
</form>
</div>

<div style="margin-top:18px">
<div class="box-title">🎨 Logo Watermark Upload</div>
<div style="background:#0a0a0a;border:1px solid #1e1e1e;border-radius:10px;padding:10px;font-size:11px;color:#666">logo_westcol.png - 32KB ✅</div>
</div>

<div style="margin-top:18px">
<div class="box-title">✏️ Subtitle Style - Color Picker for Subtitles</div>
<div class="colors">
<div class="dot" style="background:#facc15"></div>
<div class="dot" style="background:#a855f7;outline:2px solid #fff"></div>
<div class="dot" style="background:#22c55e"></div>
<div class="dot" style="background:#38bdf8"></div>
<div class="dot" style="background:#fff"></div>
<div class="dot" style="background:#f97316"></div>
</div>
<div style="margin-top:10px;display:flex;gap:8px;font-size:11px;color:#666">
<span>Font: Montserrat Bold ▼</span><span style="margin-left:auto">Auto Captions <span style="color:#22c55e">● ON</span></span>
</div>
</div>

</div>

<div class="right">
<div class="box-title">👁️ Preview Output - LIVE PREVIEW</div>
<div class="preview">
VIDEO_PREVIEW
</div>
<div class="score-box">
<div class="circle"><b>VIRAL_SCORE%</b><span>Viral Score</span><span style="font-size:7px;color:#666">High potential - Trending Hook</span></div>
<div class="hooks">
<div class="box-title">🎣 Hook Titles</div>
HOOKS_HTML
</div>
</div>
<button class="btn" onclick="document.getElementById('clips').scrollIntoView()">✨ Generate Clips Now - 6 clips • 30s each • ~1min processing</button>
<p style="color:#444;font-size:10px;text-align:center;margin-top:8px">Ready • Model: clip-gen-v2 • Credits remaining: 12/20</p>
</div>
</div>

<div id="clips" class="clips">
CLIPS_HTML
</div>

</body></html>
"""

@app.route('/')
def home():
    return HOME_HTML

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    url = request.form.get('url','') or request.args.get('url','') or "westcol-directo-01.mp4"
    
    # viral score
    viral = random.randint(88,98)
    
    # hooks
    hooks = [
        f"Este error te está costando vistas - {random.randint(85,95)}",
        f"Cómo hice {random.randint(10,50)}k en 30 días - {random.randint(80,92)}",
        f"Deja de hacer esto en tus clips - {random.randint(84,93)}",
    ]
    hooks_html = ""
    for h in hooks:
        score = random.randint(84,96)
        hooks_html += f"<div class='hook'><span>{h[:32]}</span><span>Score {score}</span></div>"

    # preview
    if "kick.com" in url.lower() or "westcol" in url.lower():
        preview = f"<div style='text-align:center'><div style='font-size:28px'>🔴</div><div style='color:#fff;font-weight:800;margin-top:4px'>WESTCOL VOD</div><div style='color:#888;font-size:10px;margin-top:2px'>{url[:50]}</div><div style='margin-top:8px;color:#a855f7;font-size:11px'>This one habit 10x'd my productivity...</div></div>"
    elif "youtube" in url.lower():
        preview = f"<div style='text-align:center;color:#fff'>▶️ YouTube Video Loaded<br><span style='color:#666;font-size:10px'>{url[:45]}</span></div>"
    elif "twitch" in url.lower():
        preview = f"<div style='text-align:center;color:#9147ff'>🟣 Twitch VOD Loaded</div>"
    else:
        preview = "Preview del clip con subtítulos amarillos/morados aquí..."

    # clips con rate morado
    clips_html = ""
    for i in range(6):
        score = random.randint(88,99)
        s = random.randint(10,600)
        title = random.choice(["POV: Te dicen esto","Nadie habla de esto","El secreto que...","3 errores que...","Así gané mi primer...","Deja de hacer esto"])
        clips_html += f"""
        <div class="clip-card">
        <div style="display:flex;justify-content:space-between;align-items:center">
        <span style="background:#a855f7;padding:4px 10px;border-radius:20px;font-weight:900;font-size:11px">{score}/100</span>
        <span style="color:#666;font-size:10px">⏱️ {s}s - {s+30}s</span>
        </div>
        <div style="margin-top:8px;font-weight:700;font-size:13px">{title}</div>
        <div style="color:#666;font-size:11px;margin-top:4px">Hook: {random.choice(hooks)[:30]}...</div>
        <div style="margin-top:10px;display:flex;gap:6px">
        <span style="background:#fff;color:#000;padding:5px 10px;border-radius:20px;font-size:11px;font-weight:800">Descargar ⬇️</span>
        <span style="background:#1e1e1e;color:#888;padding:5px 10px;border-radius:20px;font-size:11px">Copiar Hook</span>
        </div>
        </div>
        """

    page = DASH_HTML.replace("URL_VALUE", url)
    page = page.replace("VIRAL_SCORE", str(viral))
    page = page.replace("HOOKS_HTML", hooks_html)
    page = page.replace("VIDEO_PREVIEW", preview)
    page = page.replace("CLIPS_HTML", clips_html)
    return page

@app.route('/health')
def health():
    return "OK"
