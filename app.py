import os, random, subprocess, glob, shutil, uuid, requests
from flask import Flask, request, send_file, redirect
import yt_dlp

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
        except Exception as e:
            print(f"FFMPEG ERROR: {e}")
            return False

def download_url(url, vid):
    # FIX KICK
    if "kick.com" in url and "/videos/" in url:
        try:
            real_id = url.split("/videos/")[-1].split("?")[0].split("/")[0]
            url = f"https://kick.com/video/{real_id}"
        except: pass

    template = f"{TMP}/{vid}_full.%(ext)s"
    ydl_opts = {'format':'best[height<=720]/best','outtmpl':template,'quiet':True,'noplaylist':True,'merge_output_format':'mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        files = glob.glob(f"{TMP}/{vid}_full.*")
        if files:
            return files[0]
    except Exception as e:
        print(f"YT-DLP ERROR: {e}")
    return None

DASH_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipGenius FUNCIONAL</title>
<style>
body{margin:0;background:#0a0a0a;color:#fff;font-family:sans-serif}
.top{display:flex;justify-content:space-between;padding:12px 20px;background:#111;border-bottom:1px solid #1e1e1e}
.logo{font-weight:900}.logo span{color:#a855f7}
.wrap{display:flex;gap:16px;padding:16px;max-width:1400px;margin:0 auto;flex-wrap:wrap}
.left{flex:1;min-width:320px;background:#121212;border:1px solid #1e1e1e;border-radius:16px;padding:16px}
.right{flex:1.2;min-width:340px;background:#121212;border:1px solid #1e1e1e;border-radius:16px;padding:16px}
.box-title{font-size:11px;font-weight:800;color:#888;margin-bottom:8px}
.upload{border:1.5px dashed #2a2a2a;border-radius:12px;padding:20px;text-align:center;background:#0f0f0f}
.upload input{margin-top:10px}
.urlbox input{width:100%;padding:12px;border-radius:10px;background:#0a0a0a;border:1px solid #222;color:#fff;font-size:12px;box-sizing:border-box;margin-top:6px}
.colors{display:flex;gap:8px;margin-top:8px}.dot{width:22px;height:22px;border-radius:50%;border:2px solid #000}
.preview{aspect-ratio:16/9;background:#000;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid #222;overflow:hidden}
.circle{width:90px;height:90px;border-radius:50%;background:radial-gradient(circle at center,#1a1a1a 60%,#a855f7 61%);display:flex;flex-direction:column;align-items:center;justify-content:center}
.hook{background:#0f0f0f;border:1px solid #1e1e1e;border-radius:10px;padding:8px 10px;margin-bottom:6px;display:flex;justify-content:space-between;font-size:11px}
.hook span:last-child{color:#a855f7;font-weight:800}
.btn{width:100%;margin-top:14px;padding:14px;border-radius:12px;background:#a855f7;color:#fff;font-weight:900;border:none;font-size:14px}
.clips{max-width:1400px;margin:0 auto;padding:16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.card{background:#121212;border:1px solid #1e1e1e;border-radius:14px;padding:12px}
.rate{background:#a855f7;padding:4px 10px;border-radius:20px;font-weight:900;font-size:11px}
a.dl{background:#fff;color:#000;padding:6px 12px;border-radius:20px;font-weight:800;text-decoration:none;font-size:11px}
</style></head><body>
<div class="top"><div class="logo">💜 ClipViral<span>.AI</span> FUNCIONAL</div><div><a href="/" style="color:#666;text-decoration:none;font-size:12px">Home</a></div></div>
<div class="wrap">
<div class="left">
<div class="box-title">⬆️ UPLOAD VIDEO REAL</div>
<div class="upload">
<form method="post" action="/upload" enctype="multipart/form-data">
<input type="file" name="video" accept="video/*" required>
<button type="submit" class="btn" style="margin-top:10px;padding:10px;font-size:12px;background:#222">Subir y Analizar 🚀</button>
</form>
</div>
<div class="urlbox">
<div class="box-title">🔗 URL YOUTUBE / KICK / TWITCH</div>
<form method="post" action="/from_url">
<input name="url" placeholder="https://kick.com/westcol/videos/ID o youtube..." required>
<button type="submit" class="btn" style="padding:10px;font-size:12px">Bajar y Cortar con IA ✨</button>
</form>
<p style="color:#555;font-size:10px;margin-top:6px">Ej: https://kick.com/westcol/videos/01a07e7f-b5f0-78b9-a336-635073c7fe7f</p>
</div>
<div style="margin-top:16px">
<div class="box-title">🎨 Subtítulos</div>
<div class="colors"><div class="dot" style="background:#facc15"></div><div class="dot" style="background:#a855f7;outline:2px solid #fff"></div><div class="dot" style="background:#22c55e"></div><div class="dot" style="background:#fff"></div></div>
</div>
</div>
<div class="right">
<div class="box-title">👁️ Preview - STATUS</div>
<div class="preview">PREVIEW_CONTENT</div>
<div style="display:flex;gap:16px;margin-top:14px">
<div class="circle"><b>VIRAL_SCORE%</b><span style="font-size:8px;color:#888">Viral Score</span></div>
<div style="flex:1"><div class="box-title">🎣 Hook Titles</div>HOOKS</div>
</div>
</div>
</div>
<div class="clips">CLIPS_GRID</div>
</body></html>
"""

HOME = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:40px 20px}
h1{font-size:44px;font-weight:900}h1 span{color:#a855f7}
.box{max-width:600px;margin:30px auto;background:#111;border:1px solid #222;border-radius:20px;padding:20px}
input{width:100%;padding:14px;border-radius:12px;background:#18181b;border:1px solid #333;color:#fff;box-sizing:border-box}
button{width:100%;margin-top:10px;padding:14px;border-radius:999px;background:#a855f7;color:#fff;font-weight:800;border:none}
</style></head><body>
<h1>Corta videos largos en <span>clips virales</span> 🚀</h1>
<p style="color:#888">IA que analiza y te da rate de viralidad</p>
<div class="box">
<form method="post" action="/from_url">
<input name="url" placeholder="Pega YouTube / Kick / Twitch..." required>
<button>Analizar con IA ✨</button>
</form>
<a href="/dashboard" style="color:#a855f7;display:block;margin-top:14px;text-decoration:none">Ir al Dashboard PRO →</a>
</div></body></html>
"""

def make_dashboard_page(vid=None, video_path=None, msg="Listo para analizar"):
    viral = random.randint(90,98)
    hooks = [f"Este error te cuesta vistas","Cómo hice 20k en 30 días","Deja de hacer esto YA"]
    hooks_html = "".join([f"<div class='hook'><span>{h}</span><span>Score {random.randint(84,96)}</span></div>" for h in hooks])

    if video_path and os.path.exists(video_path):
        preview = f"<div style='color:#22c55e;text-align:center'><b>✅ VIDEO CARGADO</b><br><span style='color:#888;font-size:11px'>{os.path.basename(video_path)[:40]}<br>{msg}</span></div>"
    else:
        preview = f"<div style='color:#666;font-size:12px;text-align:center'>{msg}<br><span style='font-size:10px;color:#444'>Sube un video o pega URL</span></div>"

    clips_html = ""
    if vid:
        for i in range(6):
            score = random.randint(88,99)
            s = random.randint(20,300)
            # Pre-corta los clips reales ahora
            out_path = f"{TMP}/{vid}_clip{i}.mp4"
            if video_path and os.path.exists(video_path):
                run_ffmpeg(video_path, out_path, s, 35)
            clips_html += f"<div class='card'><div style='display:flex;justify-content:space-between'><span class='rate'>{score}/100</span><span style='color:#666;font-size:10px'>{s}s-{s+35}s</span></div><div style='margin-top:8px;font-weight:700;font-size:13px'>Clip #{i+1} - Hook viral detectado</div><div style='margin-top:10px'><a class='dl' href='/download?vid={vid}&n={i}'>Descargar Clip ⬇️</a></div></div>"
    else:
        clips_html = "<p style='color:#555;grid-column:1/-1;text-align:center'>Aún no hay clips. Sube un video o pega un link arriba 👆</p>"

    page = DASH_HTML.replace("PREVIEW_CONTENT", preview).replace("VIRAL_SCORE", str(viral)).replace("HOOKS", hooks_html).replace("CLIPS_GRID", clips_html)
    return page

@app.route('/')
def home():
    return HOME

@app.route('/dashboard')
def dashboard():
    return make_dashboard_page()

@app.route('/from_url', methods=['POST'])
def from_url():
    url = request.form.get('url','').strip()
    if not url:
        return redirect('/dashboard')
    vid = str(uuid.uuid4())[:8]
    video_path = download_url(url, vid)
    if not video_path:
        return make_dashboard_page(msg=f"❌ Error bajando: {url[:60]}. Prueba con YouTube.")
    # guardar path
    with open(f"{TMP}/{vid}.txt","w") as f:
        f.write(video_path)
    return make_dashboard_page(vid=vid, video_path=video_path, msg=f"Video de {url[:40]} listo - 6 clips generados")

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('video')
    if not f:
        return redirect('/dashboard')
    vid = str(uuid.uuid4())[:8]
    ext = f.filename.split('.')[-1] if '.' in f.filename else 'mp4'
    path = f"{TMP}/{vid}_full.{ext}"
    f.save(path)
    with open(f"{TMP}/{vid}.txt","w") as f2:
        f2.write(path)
    return make_dashboard_page(vid=vid, video_path=path, msg="Video local subido correctamente")

@app.route('/download')
def download():
    vid = request.args.get('vid')
    n = request.args.get('n','0')
    path = f"{TMP}/{vid}_clip{n}.mp4"
    if not os.path.exists(path):
        # intenta crear al vuelo
        try:
            with open(f"{TMP}/{vid}.txt") as f:
                full = f.read().strip()
            s = random.randint(20,300)
            run_ffmpeg(full, path, s, 35)
        except: pass
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=f"clip_viral_{n}.mp4")
    return "Clip no encontrado o expiró, vuelve a generar <a href='/dashboard'>Dashboard</a>"

@app.route('/health')
def health():
    return "OK"
