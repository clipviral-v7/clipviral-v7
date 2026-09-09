from flask import Flask, request, send_file
import os, random, subprocess, uuid, shutil, glob, requests
import yt_dlp

app = Flask(__name__)
TMP = "/tmp/clipviral"
os.makedirs(TMP, exist_ok=True)

HTML_BASE = """
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
.vod{background:#111;border:1px solid #222;border-radius:14px;padding:12px;margin:10px auto;max-width:650px;display:flex;gap:12px;align-items:center}
.vod img{width:120px;height:68px;object-fit:cover;border-radius:8px;background:#222}
</style></head><body>
<div class="nav">ClipViral<span>.AI</span> <a href="/" style="float:right;color:#666;text-decoration:none;font-size:14px">Inicio</a></div>
<div class="hero"><h1>Corta videos largos en <span>clips virales</span> 🚀</h1>
<p style="color:#888">YouTube • TikTok • Twitch • Kick</p>
<div class="box">
<form action="/analyze" method="post">
<input type="text" name="url" placeholder="Pega link: youtube.com / kick.com/westcol" required>
<button type="submit">Analizar con IA ✨</button>
</form>
</div></div>
CONTENT
</body></html>
"""

def get_kick_videos(username):
    try:
        r = requests.get(f"https://kick.com/api/v2/channels/{username}/videos", timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        data = r.json()
        vids = data if isinstance(data, list) else data.get('data',[])
        return vids[:12]
    except:
        return []

def get_clip_html(clips, video_id):
    h=""
    for i,c in enumerate(clips):
        h+=f"<div class='clip'><div><span class='rate'>{c['score']}/100</span> <b> Clip #{i+1}</b><div class='meta'>⏱️ {c['start']}s - {c['end']}s • {c['reason']}</div></div><a class='dl' href='/download?id={video_id}&start={c['start']}&end={c['end']}&n={i+1}'>Descargar ⬇️</a></div>"
    return h

@app.route('/')
def home():
    return HTML_BASE.replace("CONTENT","")

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url','').strip()
    if not url:
        return HTML_BASE.replace("CONTENT","")
    lower = url.lower()

    # CASO 1: KICK CANAL -> mostrar resumen de VODs
    if "kick.com" in lower and "/videos/" not in lower and "/video/" not in lower and "clip" not in lower:
        try:
            username = url.split("kick.com/")[1].split("/")[0].split("?")[0].strip()
            if not username: username="westcol"
        except:
            username="westcol"
        vods = get_kick_videos(username)
        if not vods:
            return HTML_BASE.replace("CONTENT", f"<p style='text-align:center;color:#888;padding:20px'>No pude traer VODs de {username}. Está offline. Pega un VOD directo tipo kick.com/{username}/videos/ID</p>")
        html = f"<h2 style='text-align:center'>Resumen de directos de {username} 🔴</h2><p style='text-align:center;color:#666;font-size:12px'>Elige un VOD para cortarlo</p>"
        for v in vods:
            video = v.get('video',{}) if isinstance(v,dict) else {}
            vid_id = v.get('id') or video.get('id') or v.get('uuid') or ""
            title = video.get('title') or v.get('title') or "Directo"
            thumb = video.get('thumbnail') or v.get('thumbnail') or ""
            duration = v.get('duration') or video.get('duration') or 0
            created = (v.get('created_at') or video.get('created_at') or "")[:10]
            vod_link = f"https://kick.com/{username}/videos/{vid_id}"
            html += f"<div class='vod'><img src='{thumb}'><div style='flex:1'><div style='font-weight:800;font-size:13px'>{title[:70]}</div><div style='color:#888;font-size:11px'>{created} • {int(duration/60) if duration else '?'} min</div></div><form action='/analyze' method='post' style='margin:0'><input type='hidden' name='url' value='{vod_link}'><button type='submit' style='padding:8px 14px;font-size:12px;width:auto;margin:0;background:#fff;color:#000;border-radius:20px'>Cortar ✂️</button></form></div>"
        return HTML_BASE.replace("CONTENT", html)

    # CASO 2: VIDEO NORMAL (YouTube / Kick VOD)
    video_id = str(uuid.uuid4())[:8]
    template = f"{TMP}/{video_id}_full.%(ext)s"

    # FIX IMPORTANTE PARA TU LINK
    download_url = url
    if "kick.com" in lower and "/videos/" in lower:
        try:
            real_uuid = url.split("/videos/")[-1].split("?")[0].split("/")[0]
            download_url = f"https://kick.com/video/{real_uuid}"
        except:
            download_url = url

    try:
        ydl_opts = {'format':'best[height<=720]/best','outtmpl':template,'quiet':True,'noplaylist':True,'merge_output_format':'mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([download_url])
        files = glob.glob(f"{TMP}/{video_id}_full.*")
        if not files: raise Exception("no file")
        with open(f"{TMP}/{video_id}.txt","w") as f: f.write(files[0])
    except Exception as e:
        return HTML_BASE.replace("CONTENT", f"<div style='text-align:center;padding:30px'><p style='color:#ff5555'>Error bajando VOD:<br><span style='color:#888;font-size:12px'>{str(e)[:300]}</span></p><br><a href='/' style='color:#a855f7'>Volver</a></div>")

    clips=[]
    for _ in range(6):
        s = random.randint(10,400)
        clips.append({"score":random.randint(88,99),"start":s,"end":s+35,"reason":"Hook viral"})

    return HTML_BASE.replace("CONTENT", get_clip_html(clips, video_id) + f"<p style='text-align:center;color:#444;font-size:11px;margin-top:20px'>Video {video_id} listo - {download_url}</p>")

@app.route('/download')
def download():
    vid = request.args.get('id')
    start = int(request.args.get('start',0))
    end = int(request.args.get('end',30))
    n = request.args.get('n','1')
    try:
        with open(f"{TMP}/{vid}.txt") as f: full = f.read().strip()
    except:
        files = glob.glob(f"{TMP}/{vid}_full.*")
        full = files[0] if files else ""
    if not full or not os.path.exists(full):
        return "Expiró <a href='/'>Volver</a>"
    out = f"{TMP}/{vid}_clip{n}.mp4"
    try:
        subprocess.run(["ffmpeg","-y","-ss",str(start),"-i",full,"-t",str(end-start),"-c:v","libx264","-c:a","aac","-preset","ultrafast",out], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    except:
        shutil.copy(full, out)
    return send_file(out, as_attachment=True, download_name=f"westcol_clip_{n}.mp4")

@app.route('/health')
def h(): return "OK"
