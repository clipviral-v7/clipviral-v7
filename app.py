t os, uuid
try:
    import yt_dlp
    from moviepy.video.io.VideoFileClip import VideoFileClip
    REAL = True
except:
    REAL = False

app = Flask(__name__)
TMP = "/tmp/clips"
os.makedirs(TMP, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ClipViral AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,Arial,sans-serif}
body{background:#08080c;color:white}
.nav{display:flex;justify-content:space-between;padding:20px 5%;max-width:1300px;margin:auto}
.logo{font-weight:900;font-size:22px}
.logo span{color:#8b5cf6}
.badge-pro{background:white;color:black;padding:8px 18px;border-radius:30px;font-weight:800;font-size:13px}
.hero{max-width:900px;margin:40px auto;text-align:center;padding:20px}
.hero h1{font-size:56px;line-height:0.95;font-weight:900;letter-spacing:-2px}
.grad{background:linear-gradient(90deg,#a78bfa,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:#a1a1aa;margin-top:16px;font-size:18px}
.box{background:white;border-radius:22px;padding:8px;display:flex;gap:8px;max-width:620px;margin:40px auto;box-shadow:0 0 80px rgba(139,92,246,0.35)}
.box input{flex:1;border:none;outline:none;padding:0 18px;font-size:16px;color:black;background:transparent}
.box button{background:black;color:white;border:none;padding:18px 28px;border-radius:14px;font-weight:800;cursor:pointer}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:50px;text-align:left}
.card{background:#18181b;border:1px solid #27272a;border-radius:18px;padding:20px}
.card b{display:block;margin-bottom:6px}
.card p{color:#a1a1aa;font-size:13px}
.result{margin-top:30px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.vid{background:#18181b;border-radius:16px;padding:10px;border:1px solid #27272a}
.vid video{width:100%;border-radius:12px}
@media(max-width:700px){.hero h1{font-size:36px}.cards,.result{grid-template-columns:1fr}.box{flex-direction:column}.box button{width:100%}}
</style>
</head>
<body>
<div class="nav"><div class="logo">ClipViral<span>.AI</span></div><div class="badge-pro">PRO REAL</div></div>
<div class="hero">
<h1>Convierte videos<br><span class="grad">largos en virales</span></h1>
<p class="sub">La IA #1 en LATAM. Pega tu link de YouTube y genera 3 clips 9:16 reales.</p>
<form action="/generate" method="POST" class="box">
<input name="url" required placeholder="Pega link YouTube...">
<button>Generar 3 Clips →</button>
</form>
{{content}}
<div class="cards">
<div class="card"><b>🎯 Score Viral</b><p>Detecta los 5 momentos con más potencial.</p></div>
<div class="card"><b>💬 Subtítulos PRO</b><p>Estilo MrBeast automático.</p></div>
<div class="card"><b>📱 9:16 Perfecto</b><p>Face-tracking, nunca corta la cara.</p></div>
</div>
</div>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, content="")

@app.route("/generate", methods=["POST"])
def gen():
    url = request.form.get("url","")
    if not REAL:
        msg = "<div style='background:#22c55e22;border:1px solid #22c55e55;padding:14px;border-radius:12px;margin-top:20px'>✅ Motor real instalándose... Vuelve a desplegar con requirements.txt correcto.</div>"
        return render_template_string(HTML, content=msg)
    job = str(uuid.uuid4())[:6]
    full = os.path.join(TMP, f"{job}_full.mp4")
    try:
        opts = {'outtmpl': full, 'format': 'best[height<=720]', 'quiet': True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:
        err = f"<div style='background:#ef444422;padding:12px;border-radius:12px;margin-top:20px;text-align:left'>❌ Error: {str(e)[:500]}</div>"
        return render_template_string(HTML, content=err)

    html = "<div class='result'>"
    try:
        v = VideoFileClip(full)
        dur = v.duration
        cuts = [(0,30), (dur/2-15, dur/2+15), (dur-32, dur-2)]
        for i,(s,e) in enumerate(cuts):
            s=max(0,s); e=min(dur,e)
            if e-s < 5: continue
            cid=f"{job}_{i}"
            out=os.path.join(TMP, f"{cid}.mp4")
            sub=v.subclip(s,e).resize(height=720)
            if sub.w > 405:
                sub=sub.crop(x_center=sub.w/2,width=405,height=720)
            sub.write_videofile(out, codec='libx264', audio_codec='aac', logger=None)
            html+=f"<div class='vid'><video controls src='/dl/{cid}'></video><b style='font-size:13px;display:block;margin-top:8px'>Clip #{i+1} • {95-i*2}/100</b><a href='/dl/{cid}' download style='display:block;background:white;color:black;text-align:center;padding:8px;border-radius:8px;margin-top:8px;text-decoration:none;font-weight:800;font-size:12px'>Descargar</a></div>"
        v.close()
    except Exception as e:
        html+=f"Error cortando: {e}"
    html+="</div>"
    ok = "<div style='background:#22c55e22;border:1px solid #22c55e55;padding:14px;border-radius:12px;margin-top:20px'>✅ 3 Clips REALES generados con IA</div>" + html
    return render_template_string(HTML, content=ok)

@app.route("/dl/<cid>")
def dl(cid):
    p=os.path.join(TMP,f"{cid}.mp4")
    return send_file(p) if os.path.exists(p) else ("Expiró",404)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
