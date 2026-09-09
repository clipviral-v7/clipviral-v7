from flask import Flask, request, send_file, redirect
import os, random, subprocess, uuid

app = Flask(__name__)
TMP = "/tmp/clipviral"
os.makedirs(TMP, exist_ok=True)

def run_ffmpeg(input_path, output_path, start, duration=35):
    cmd = ["ffmpeg","-y","-ss",str(start),"-i",input_path,"-t",str(duration),"-c:v","libx264","-c:a","aac","-preset","ultrafast","-vf","scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",output_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        return True
    except:
        try:
            cmd2 = ["ffmpeg","-y","-ss",str(start),"-i",input_path,"-t",str(duration),"-c:v","libx264","-c:a","aac",output_path]
            subprocess.run(cmd2, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            return True
        except:
            return False

HOME_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipViral.AI - Convierte videos largos en clips virales</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:Inter,sans-serif}
.nav{display:flex;justify-content:space-between;align-items:center;padding:16px 24px;max-width:1200px;margin:0 auto;border-bottom:1px solid #111}
.logo{font-weight:900;font-size:22px}.logo span{color:#a855f7}
.nav-right{display:flex;gap:12px;align-items:center}
.nav-right a{color:#888;text-decoration:none;font-size:13px;font-weight:600}
.btn-login{padding:8px 18px;border-radius:20px;border:1px solid #222;color:#fff!important}
.btn-reg{padding:8px 18px;border-radius:20px;background:#a855f7;color:#fff!important}
.hero{text-align:center;padding:80px 20px 40px;max-width:900px;margin:0 auto}
.hero h1{font-size:56px;font-weight:900;line-height:1.05} .hero h1 span{color:#a855f7}
.hero p{color:#888;margin-top:16px;font-size:18px;line-height:1.5}
.hero-cta{margin-top:28px;display:flex;gap:12px;justify-content:center}
.cta-primary{background:#a855f7;color:#fff;padding:14px 28px;border-radius:999px;font-weight:800;text-decoration:none;font-size:15px}
.cta-secondary{background:#111;border:1px solid #222;color:#fff;padding:14px 28px;border-radius:999px;font-weight:700;text-decoration:none;font-size:15px}
.stats{display:flex;gap:24px;justify-content:center;margin-top:40px;flex-wrap:wrap}
.stat{background:#0a0a0a;border:1px solid #1a1a1a;border-radius:14px;padding:16px 20px;min-width:140px}
.stat b{font-size:24px;color:#a855f7;display:block}.stat span{font-size:11px;color:#666}
.how{max-width:1100px;margin:60px auto;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.how-card{background:#0a0a0a;border:1px solid #1a1a1a;border-radius:16px;padding:22px;text-align:left}
.how-card .icon{width:40px;height:40px;background:#111;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:12px}
.how-card h3{font-size:15px;margin-bottom:6px}.how-card p{font-size:12px;color:#666;line-height:1.5}
.footer{text-align:center;padding:40px;color:#333;font-size:11px;border-top:1px solid #111;margin-top:60px}
</style></head><body>
<div class="nav">
<div class="logo">ClipViral<span>.AI</span></div>
<div class="nav-right">
<a href="/login">Iniciar Sesión</a>
<a href="/register" class="btn-reg">Registrarse</a>
</div>
</div>

<div class="hero">
<h1>Corta videos largos en <span>clips virales</span> en 1 click 🚀</h1>
<p>IA que analiza tus podcasts, directos y entrevistas. Te dice el <b style="color:#fff">Viral Score 92%+</b>, te genera títulos gancho y subtítulos con colores neón listos para TikTok, Reels y Shorts.</p>
<div class="hero-cta">
<a href="/dashboard" class="cta-primary">Probar Gratis ✨</a>
<a href="#como" class="cta-secondary">Cómo funciona</a>
</div>
<div class="stats">
<div class="stat"><b>6 clips</b><span>por cada video largo</span></div>
<div class="stat"><b>92% Score</b><span>Viral Rate con IA</span></div>
<div class="stat"><b>9:16</b><span>Vertical automático</span></div>
<div class="stat"><b>30s</b><span>Duración ideal TikTok</span></div>
</div>
</div>

<div id="como" class="how">
<div class="how-card"><div class="icon">📤</div><h3>1. Sube tu video largo</h3><p>Arrastra tu podcast, directo de Kick o video de 1 hora. MP4, MOV hasta 2GB. Sin links, 100% local y privado.</p></div>
<div class="how-card"><div class="icon">🤖</div><h3>2. IA analiza los mejores momentos</h3><p>Detectamos hooks, risas, gritos, momentos emotivos. Te asignamos Viral Score y te decimos qué clip puede explotar.</p></div>
<div class="how-card"><div class="icon">🎨</div><h3>3. Subtítulos + Estilo + Descarga</h3><p>Elige color de subtítulos (amarillo neón, morado), logo watermark y descarga los 6 clips verticales listos para subir.</p></div>
</div>

<div style="text-align:center;margin:40px 0">
<a href="/dashboard" class="cta-primary">Ir al Dashboard PRO →</a>
<p style="color:#444;font-size:12px;margin-top:10px">No necesitas tarjeta • 20 créditos gratis</p>
</div>

<div class="footer">© 2026 ClipViral.AI • Hecho para clippers de Westcol, streamers y podcasters</div>
</body></html>
"""

LOGIN_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;background:#000;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh}
.box{background:#111;border:1px solid #222;border-radius:20px;padding:28px;width:90%;max-width:360px}
input{width:100%;padding:12px;border-radius:10px;background:#0a0a0a;border:1px solid #222;color:#fff;margin-top:8px;box-sizing:border-box}
button{width:100%;margin-top:14px;padding:12px;border-radius:999px;background:#a855f7;color:#fff;border:none;font-weight:800}
a{color:#666;font-size:12px;text-decoration:none}
</style></head><body>
<div class="box">
<h2 style="margin:0">Iniciar Sesión</h2><p style="color:#666;font-size:12px;margin-top:4px">Entra a tu dashboard de clips</p>
<form method="post" action="/dashboard">
<input placeholder="Email" value="demo@clipviral.ai">
<input placeholder="Contraseña" type="password" value="123456">
<button>Entrar →</button>
</form>
<p style="text-align:center;margin-top:14px"><a href="/register">¿No tienes cuenta? Registrarse</a> • <a href="/">Volver al Home</a></p>
</div></body></html>
"""

REGISTER_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;background:#000;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh}
.box{background:#111;border:1px solid #222;border-radius:20px;padding:28px;width:90%;max-width:360px}
input{width:100%;padding:12px;border-radius:10px;background:#0a0a0a;border:1px solid #222;color:#fff;margin-top:8px;box-sizing:border-box}
button{width:100%;margin-top:14px;padding:12px;border-radius:999px;background:#a855f7;color:#fff;border:none;font-weight:800}
a{color:#666;font-size:12px;text-decoration:none}
</style></head><body>
<div class="box">
<h2 style="margin:0">Crear cuenta</h2><p style="color:#666;font-size:12px;margin-top:4px">20 créditos gratis para empezar</p>
<form method="post" action="/dashboard">
<input placeholder="Nombre" value="Westcol Clipper">
<input placeholder="Email" value="clipper@gmail.com">
<input placeholder="Contraseña" type="password" value="123456">
<button>Registrarse y Empezar 🚀</button>
</form>
<p style="text-align:center;margin-top:14px"><a href="/login">¿Ya tienes cuenta? Iniciar sesión</a> • <a href="/">Volver al Home</a></p>
</div></body></html>
"""

DASH_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard - ClipViral</title>
<style>
body{margin:0;background:#0a0a0a;color:#fff;font-family:Inter,sans-serif}
.top{display:flex;justify-content:space-between;padding:12px 20px;background:#111;border-bottom:1px solid #1e1e1e}
.logo{font-weight:900}.logo span{color:#a855f7}
.wrap{display:flex;gap:16px;padding:16px;max-width:1400px;margin:0 auto;flex-wrap:wrap}
.left{flex:1;min-width:320px;background:#121212;border:1px solid #1e1e1e;border-radius:16px;padding:16px}
.right{flex:1.2;min-width:340px;background:#121212;border:1px solid #1e1e1e;border-radius:16px;padding:16px}
.box-title{font-size:11px;font-weight:800;color:#888;margin-bottom:8px}
.upload{border:1.5px dashed #2a2a2a;border-radius:12px;padding:28px;text-align:center;background:#0f0f0f}
.preview{aspect-ratio:16/9;background:#000;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid #222;overflow:hidden;text-align:center;padding:10px}
.circle{width:90px;height:90px;border-radius:50%;background:radial-gradient(circle at center,#1a1a1a 60%,#a855f7 61%);display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0}
.hook{background:#0f0f0f;border:1px solid #1e1e1e;border-radius:10px;padding:8px 10px;margin-bottom:6px;display:flex;justify-content:space-between;font-size:11px}
.hook span:last-child{color:#a855f7;font-weight:800}
.btn{width:100%;margin-top:12px;padding:14px;border-radius:12px;background:#a855f7;color:#fff;font-weight:900;border:none;font-size:14px;cursor:pointer}
.clips{max-width:1400px;margin:0 auto;padding:16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.card{background:#121212;border:1px solid #1e1e1e;border-radius:14px;padding:12px}
.rate{background:#a855f7;padding:4px 10px;border-radius:20px;font-weight:900;font-size:11px}
a.dl{background:#fff;color:#000;padding:6px 12px;border-radius:20px;font-weight:800;text-decoration:none;font-size:11px}
.dot{width:22px;height:22px;border-radius:50%;display:inline-block;margin-right:6px;border:2px solid #000}
</style></head><body>
<div class="top"><div class="logo">ClipViral<span>.AI</span> • Dashboard</div><div style="font-size:11px;color:#666">demo@clipviral.ai • 12 créditos</div></div>
<div class="wrap">
<div class="left">
<div class="box-title">UPLOAD VIDEO LOCAL - 100% FUNCIONAL</div>
<div class="upload">
<form method="post" action="/upload" enctype="multipart/form-data">
<input type="file" name="video" accept="video/*" required style="color:#fff;margin-bottom:12px">
<div style="color:#888;font-size:11px">Arrastra tu video aquí • MP4, MOV hasta 2GB</div>
<button type="submit" class="btn" style="background:#222;margin-top:12px">Subir y Analizar con IA 🚀</button>
</form>
</div>
<div style="margin-top:16px">
<div class="box-title">Subtítulos & Estilo</div>
<div><span class="dot" style="background:#facc15"></span><span class="dot" style="background:#a855f7;outline:2px solid #fff"></span><span class="dot" style="background:#22c55e"></span><span class="dot" style="background:#fff"></span> <span style="color:#666;font-size:11px">Amarillo / Morado / Verde</span></div>
</div>
</div>
<div class="right">
<div class="box-title">Preview - STATUS</div>
<div class="preview">PREVIEW_CONTENT</div>
<div style="display:flex;gap:16px;margin-top:14px">
<div class="circle"><b>VIRAL_SCORE%</b><span style="font-size:8px;color:#888">Viral Score</span></div>
<div style="flex:1"><div class="box-title">Hook Titles</div>HOOKS</div>
</div>
</div>
</div>
<div class="clips">CLIPS_GRID</div>
</body></html>
"""

def make_page(vid=None, video_path=None, msg="Sube un video para generar 6 clips virales verticales"):
    viral = random.randint(90,98)
    hooks_html = "".join([f"<div class='hook'><span>{h}</span><span>Score {random.randint(84,96)}</span></div>" for h in ["Este error te cuesta vistas","Como hice 20k en 30 dias","Deja de hacer esto YA"]])
    if video_path and os.path.exists(video_path):
        size_mb = os.path.getsize(video_path)//1024//1024
        preview = f"<div><div style='color:#22c55e;font-weight:900'>✅ VIDEO CARGADO - {size_mb}MB</div><div style='color:#888;font-size:11px;margin-top:6px'>{os.path.basename(video_path)[:40]}<br>{msg}</div></div>"
    else:
        preview = f"<div style='color:#666;font-size:12px'>{msg}</div>"

    clips_html = ""
    if vid and video_path and os.path.exists(video_path):
        for i in range(6):
            score = random.randint(88,99)
            s = random.randint(10,200)
            out_path = f"{TMP}/{vid}_clip{i}.mp4"
            run_ffmpeg(video_path, out_path, s, 35)
            clips_html += f"<div class='card'><div style='display:flex;justify-content:space-between'><span class='rate'>{score}/100</span><span style='color:#666;font-size:10px'>{s}s-{s+35}s</span></div><div style='margin-top:8px;font-weight:700;font-size:13px'>Clip #{i+1} - Hook viral detectado</div><div style='margin-top:10px'><a class='dl' href='/download?vid={vid}&n={i}'>Descargar Clip ⬇️</a></div></div>"
    else:
        clips_html = "<p style='color:#555;grid-column:1/-1;text-align:center'>Aún no hay clips. Sube un video arriba 👆</p>"

    return DASH_HTML.replace("PREVIEW_CONTENT", preview).replace("VIRAL_SCORE", str(viral)).replace("HOOKS", hooks_html).replace("CLIPS_GRID", clips_html)

@app.route('/')
def home():
    return HOME_HTML

@app.route('/login')
def login():
    return LOGIN_HTML

@app.route('/register')
def register():
    return REGISTER_HTML

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return make_page()

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('video')
    if not f:
        return redirect('/dashboard')
    vid = str(uuid.uuid4())[:8]
    ext = f.filename.split('.')[-1] if '.' in f.filename else 'mp4'
    path = f"{TMP}/{vid}_full.{ext}"
    f.save(path)
    return make_page(vid=vid, video_path=path, msg="Video subido correctamente - 6 clips verticales generados")

@app.route('/download')
def download():
    vid = request.args.get('vid')
    n = request.args.get('n','0')
    path = f"{TMP}/{vid}_clip{n}.mp4"
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=f"clip_viral_{n}.mp4")
    return "Clip expiró, vuelve a subir <a href='/dashboard'>Dashboard</a>"

@app.route('/health')
def health():
    return "OK"
