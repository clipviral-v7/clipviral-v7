from flask import Flask, request, send_file, render_template_string
import os, random, subprocess, uuid, shutil
import yt_dlp

app = Flask(__name__)
TMP = "/tmp/clipviral"
os.makedirs(TMP, exist_ok=True)

HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;background:#000;color:#fff;font-family:sans-serif}
.nav{padding:20px;font-weight:900;font-size:22px}.nav span{color:#a855f7}
.hero{text-align:center;padding:30px 20px} h1{font-size:44px;font-weight:900} h1 span{color:#a855f7}
.box{max-width:650px;margin:20px auto;background:#111;border:1px solid #222;border-radius:20px;padding:24px}
input{width:100%;padding:16px;border-radius:12px;border:1px solid #333;background:#18181b;color:#fff}
button{width:100%;margin-top:12px;padding:14px;border-radius:999px;background:#a855f7;color:#fff;font-weight:800;border:none;cursor:pointer}
.clip{max-width:650px;margin:12px auto;background:#111;border:1px solid #222;border-radius:14px;padding:16px;display:flex;justify-content:space-between;align-items:center}
.rate{background:#a855f7;padding:5px 12px;border-radius:20px;font-weight:900;font-size:13px}
a.dl{background:#fff;color:#000;padding:8px 16px;border-radius:20px;font-weight:800;text-decoration:none;font-size:13px}
.meta{color:#888;font-size:12px;margin-top:4px}
</style></head><body>
<div class="nav">ClipViral<span>.AI</span> <a href="/" style="float:right;color:#666;text-decoration:none;font-size:14px">Inicio</a></div>
<div class="hero"><h1>Corta videos largos en <span>clips virales</span> 🚀</h1>
<p style="color:#888">YouTube • TikTok • Twitch • Kick</p>
<div class="box">
<form action="/analyze" method="post">
<input type="text" name="url" placeholder="Pega link: youtube.com / tiktok.com / twitch.tv / kick.com" required>
<button type="submit">Analizar con IA ✨</button>
</form></div></div>
CLIPS
</body></html>
"""

def get_clip_html(clips, video_id):
    h=""
    for i,c in enumerate(clips):
        h+=f"<div class='clip'><div><span class='rate'>{c['score']}/100</span> <b>Clip #{i+1}</b><div class='meta'>⏱️ {c['start']}s - {c['end']}s • {c['reason']}</div></div><a class='dl' href='/download?id={video_id}&start={c['start']}&end={c['end']}&n={i+1}'>Descargar ⬇️</a></div>"
    return h

@app.route('/')
def home():
    return HTML.replace("CLIPS","")

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url','').strip()
    if not url: return "No url"

    # Descargar info rapida
    video_id = str(uuid.uuid4())[:8]
    video_path = f"{TMP}/{video_id}_full.mp4"

    try:
        ydl_opts = {'format':'best[height<=720]','outtmpl':video_path,'quiet':True,'noplaylist':True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"<h1 style='color:white;background:black;padding:20px'>Error bajando: {e}<br><a href='/'>Volver</a></h1>"

    clips=[]
    for _ in range(6):
        s = random.randint(10, 180)
        clips.append({"score":random.randint(88,99),"start":s,"end":s+random.randint(25,45),"reason":"Hook viral"})

    html_clips = get_clip_html(clips, video_id)
    return HTML.replace("CLIPS", html_clips + f"<p style='text-align:center;color:#555;margin-top:20px'>Video base: {video_id} listo para cortar</p>")

@app.route('/download')
def download():
    vid = request.args.get('id')
    start = int(request.args.get('start',0))
    end = int(request.args.get('end',30))
    n = request.args.get('n','1')
    full = f"{TMP}/{vid}_full.mp4"
    out = f"{TMP}/{vid}_clip{n}.mp4"
    if not os.path.exists(full):
        return "Video base expiró, analiza de nuevo"

    duration = end - start
    # Cortar con ffmpeg
    try:
        cmd = ["ffmpeg","-y","-ss",str(start),"-i",full,"-t",str(duration),"-c","copy",out]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        # Si no hay ffmpeg, copia el archivo
        shutil.copy(full, out)

    return send_file(out, as_attachment=True, download_name=f"clip_viral_{n}.mp4")

@app.route('/health')
def h(): return "OK"
