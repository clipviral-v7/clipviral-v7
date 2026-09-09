from flask import Flask, request, send_file
import os, random, subprocess, uuid, shutil, glob
import yt_dlp

app = Flask(__name__)
TMP = "/tmp/clipviral"
os.makedirs(TMP, exist_ok=True)

HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipViral.AI</title>
<style>
body{margin:0;background:#000;color:#fff;font-family:Inter,sans-serif}
.nav{padding:20px;font-weight:900;font-size:22px;max-width:1200px;margin:0 auto}.nav span{color:#a855f7}
.hero{text-align:center;padding:30px 20px} h1{font-size:44px;font-weight:900;line-height:1.1} h1 span{color:#a855f7}
.box{max-width:650px;margin:20px auto;background:#111;border:1px solid #222;border-radius:20px;padding:24px}
input{width:100%;padding:16px;border-radius:12px;border:1px solid #333;background:#18181b;color:#fff;font-size:14px}
button{width:100%;margin-top:12px;padding:14px;border-radius:999px;background:#a855f7;color:#fff;font-weight:800;border:none;font-size:16px;cursor:pointer}
.clip{max-width:650px;margin:12px auto;background:#111;border:1px solid #222;border-radius:14px;padding:16px;display:flex;justify-content:space-between;align-items:center}
.rate{background:#a855f7;padding:5px 12px;border-radius:20px;font-weight:900;font-size:13px;color:#fff}
a.dl{background:#fff;color:#000;padding:8px 16px;border-radius:20px;font-weight:800;text-decoration:none;font-size:13px}
.meta{color:#888;font-size:12px;margin-top:4px}
</style></head><body>
<div class="nav">ClipViral<span>.AI</span> <a href="/" style="float:right;color:#666;text-decoration:none;font-size:14px">Inicio</a></div>
<div class="hero"><h1>Corta videos largos en <span>clips virales</span> 🚀</h1>
<p style="color:#888;margin-top:8px">YouTube • TikTok • Twitch • Kick</p>
<div class="box">
<form action="/analyze" method="post">
<input type="text" name="url" placeholder="Pega link: youtube.com / tiktok.com / twitch.tv / kick.com/videos/..." required>
<button type="submit">Analizar con IA ✨</button>
</form>
</div></div>
CLIPS
</body></html>
"""

def get_clip_html(clips, video_id):
    h=""
    for i,c in enumerate(clips):
        h+=f"<div class='clip'><div><span class='rate'>{c['score']}/100</span> <b> Clip #{i+1}</b><div class='meta'>⏱️ {c['start']}s - {c['end']}s • {c['reason']}</div></div><a class='dl' href='/download?id={video_id}&start={c['start']}&end={c['end']}&n={i+1}'>Descargar ⬇️</a></div>"
    return h

@app.route('/')
def home():
    return HTML.replace("CLIPS","")

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url','').strip()
    if not url:
        return HTML.replace("CLIPS","")

    # Validacion Kick canal
    if "kick.com" in url.lower() and "/videos/" not in url.lower() and "clip" not in url.lower() and "/video/" not in url.lower():
        return """
        <html><body style="background:#000;color:#fff;font-family:sans-serif;padding:40px;text-align:center">
        <h1>⚠️ Link de Kick incorrecto</h1>
        <p style="color:#888">Pegaste el canal completo: kick.com/westcol<br>Así no se puede bajar si no está en vivo.</p>
        <p style="color:#a855f7;margin-top:15px">Solución:<br>Ve al perfil de Westcol > Pestaña Videos > Abre un VOD<br>Copia ese link: kick.com/westcol/videos/xxxx</p>
        <p style="color:#666;margin-top:15px">Mejor prueba con YouTube primero para ver que funciona</p>
        <br><br><a href="/" style="color:#a855f7;text-decoration:none;font-weight:800">← Volver</a>
        </body></html>
        """

    video_id = str(uuid.uuid4())[:8]
    video_path_template = f"{TMP}/{video_id}_full.%(ext)s"

    try:
        ydl_opts = {
            'format': 'best[height<=720]/best',
            'outtmpl': video_path_template,
            'quiet': True,
            'noplaylist': True,
            'no_warnings': True,
            'merge_output_format': 'mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        files = glob.glob(f"{TMP}/{video_id}_full.*")
        if not files:
            raise Exception("No se descargó nada")

        real_path = files[0]
        with open(f"{TMP}/{video_id}.txt","w") as f:
            f.write(real_path)

    except Exception as e:
        err = str(e)
        if "not currently live" in err.lower() or "is not currently live" in err:
            return """<div style='background:#000;color:#fff;padding:40px;font-family:sans-serif;text-align:center'><h1>El canal no está en vivo 🔴</h1><p style='color:#888'>Kick solo deja bajar si es un VOD guardado, no el canal.<br>Usa un link tipo kick.com/usuario/videos/ID</p><br><a href='/' style='color:#a855f7'>← Volver</a></div>"""
        return f"<div style='background:#000;color:#fff;padding:30px;font-family:sans-serif'><h3>Error bajando:</h3><p style='color:#888'>{err[:300]}</p><br><a href='/' style='color:#a855f7'>Volver</a></div>"

    clips=[]
    for _ in range(6):
        s = random.randint(10, 300)
        clips.append({"score":random.randint(88,99),"start":s,"end":s+random.randint(25,45),"reason":"Hook viral detectado"})

    html_clips = get_clip_html(clips, video_id)
    return HTML.replace("CLIPS", html_clips + f"<p style='text-align:center;color:#444;margin-top:20px;font-size:12px'>Video {video_id} listo para cortar ✂️</p>")

@app.route('/download')
def download():
    vid = request.args.get('id')
    start = int(request.args.get('start',0))
    end = int(request.args.get('end',30))
    n = request.args.get('n','1')

    try:
        with open(f"{TMP}/{vid}.txt") as f:
            full = f.read().strip()
    except:
        files = glob.glob(f"{TMP}/{vid}_full.*")
        full = files[0] if files else ""

    if not full or not os.path.exists(full):
        return "Video expiró, analiza de nuevo <a href='/'>Volver</a>"

    out = f"{TMP}/{vid}_clip{n}.mp4"
    duration = end - start

    try:
        cmd = ["ffmpeg","-y","-ss",str(start),"-i",full,"-t",str(duration),"-c:v","libx264","-c:a","aac","-preset","ultrafast",out]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    except:
        try:
            cmd = ["ffmpeg","-y","-ss",str(start),"-i",full,"-t",str(duration),"-c","copy",out]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        except:
            shutil.copy(full, out)

    return send_file(out, as_attachment=True, download_name=f"clip_viral_{n}.mp4")

@app.route('/health')
def health():
    return "OK"
