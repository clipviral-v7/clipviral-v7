from flask import Flask, render_template_string
app = Flask(__name__)

# LANDING PAGE - Presentación
LANDING = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipViral.AI - Convierte videos largos en virales</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,system-ui,sans-serif}
body{background:#08080a;color:white;overflow-x:hidden}
.nav{display:flex;justify-content:space-between;align-items:center;padding:18px 40px;position:fixed;width:100%;background:rgba(8,8,10,.8);backdrop-filter:blur(12px);z-index:10;border-bottom:1px solid #1a1a1e}
.logo{font-weight:900;font-size:20px}.logo span{color:#a855f7}
.menu{display:flex;gap:12px;align-items:center}
.btn-white{background:#fff;color:#000;padding:10px 18px;border-radius:20px;font-weight:800;font-size:13px;text-decoration:none}
.btn-ghost{color:#999;text-decoration:none;font-size:13px;padding:10px}
.hero{padding:160px 20px 80px;text-align:center;max-width:900px;margin:0 auto}
.hero h1{font-size:72px;line-height:.9;font-weight:900;letter-spacing:-2px}
.hero h1 span{background:linear-gradient(90deg,#a78bfa,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:#888;margin:20px auto;max-width:500px;font-size:18px}
.hero-cta{display:flex;gap:12px;justify-content:center;margin-top:30px}
.btn-big{padding:16px 32px;border-radius:12px;font-weight:900;font-size:16px;text-decoration:none;display:inline-block}
.btn-morado{background:linear-gradient(90deg,#8b5cf6,#a78bfa);color:white}
.btn-negro{background:#1a1a1e;color:white;border:1px solid #2a2a2e}
.features{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1000px;margin:60px auto;padding:0 20px}
.feat{background:#121214;border:1px solid #1e1e22;border-radius:16px;padding:24px;text-align:left}
.feat b{font-size:16px}.feat p{font-size:13px;color:#777;margin-top:8px;line-height:1.4}
.demo{max-width:1000px;margin:60px auto;padding:0 20px;text-align:center}
.demo img{width:100%;border-radius:20px;border:1px solid #2a2a2e;box-shadow:0 20px 60px rgba(139,92,246,.2)}
@media(max-width:700px){.hero h1{font-size:40px}.features{grid-template-columns:1fr}.nav{padding:14px 20px}}
</style></head>
<body>
<div class="nav"><div class="logo">ClipViral<span>.AI</span></div><div class="menu"><a class="btn-ghost" href="#features">Features</a><a class="btn-white" href="/dashboard">Entrar al Dashboard →</a></div></div>
<div class="hero">
<h1>Convierte videos<br><span>largos en virales</span></h1>
<p>La IA #1 en LATAM. Sube tu podcast, directo o video de 3 horas y te genera 10 clips listos para TikTok, Reels y Shorts con subtítulos estilo MrBeast.</p>
<div class="hero-cta"><a href="/dashboard" class="btn-big btn-morado">✨ Probar Gratis Ahora</a><a href="#demo" class="btn-big btn-negro">Ver Demo</a></div>
<p style="margin-top:16px;font-size:12px;color:#555">Sin tarjeta • 3 clips gratis • Cancela cuando quieras</p>
</div>
<div id="features" class="features">
<div class="feat"><b>🎯 Score Viral 92%</b><p>Nuestra IA detecta los 5 momentos con más potencial de viralización de tu video largo.</p></div>
<div class="feat"><b>💬 Subtítulos PRO Animados</b><p>Estilo Hormozi / MrBeast automático con color picker. Yellow, purple, pink, neon.</p></div>
<div class="feat"><b>📱 9:16 Perfecto con Face-Tracking</b><p>Recorta automático siguiendo tu cara. Listo para subir a TikTok sin editar.</p></div>
</div>
<div id="demo" class="demo"><h2 style="margin-bottom:20px">Dashboard PRO como lo usan los grandes</h2><div style="background:#151122;border:1px solid #2a2540;border-radius:16px;padding:10px"><div style="background:#000;border-radius:12px;padding:40px;color:#8b7fb0">Preview de tu Dashboard aquí → <a href="/dashboard" style="color:#a78bfa">Entrar</a></div></div></div>
<div style="text-align:center;padding:60px;color:#444;font-size:12px">© 2026 ClipViral.AI • Hecho en Colombia 🇨🇴</div>
</body></html>
"""

# DASHBOARD - El que ya tienes (92% score)
DASHBOARD = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard - ClipViral.AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,system-ui,sans-serif}
body{background:#0e0a1f;color:white}
.nav{background:#151122;display:flex;justify-content:space-between;align-items:center;padding:14px 24px;border-bottom:1px solid #2a2540}
.logo{display:flex;align-items:center;gap:8px;font-weight:900;text-decoration:none;color:white}
.logo-icon{width:28px;height:28px;background:linear-gradient(135deg,#a78bfa,#f472b6);border-radius:8px;display:grid;place-items:center}
.menu{display:flex;gap:20px;color:#8b7fb0;font-size:13px;align-items:center}
.menu b{color:white}.menu a{color:#8b7fb0;text-decoration:none}
.wrap{display:grid;grid-template-columns:380px 1fr;gap:20px;max-width:1200px;margin:20px auto;padding:0 20px}
.card{background:#1a1630;border:1px solid #2a2540;border-radius:16px;padding:18px}
.card h3{font-size:13px;color:#a89ccf;margin-bottom:12px}
.upload{border:1px dashed #3a3560;border-radius:12px;padding:30px;text-align:center;color:#6b6490;font-size:13px;background:#151122;cursor:pointer}
.upload b{color:#a78bfa}
.field{background:#151122;border:1px solid #2a2540;border-radius:10px;padding:12px;margin-top:10px;display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#8b7fb0}
.colors{display:flex;gap:8px;margin-top:10px}.dot{width:22px;height:22px;border-radius:50%;border:2px solid #2a2540;cursor:pointer}.dot.active{border-color:white}
.toggle{width:36px;height:20px;background:#3a3560;border-radius:20px;position:relative}.toggle::after{content:'';position:absolute;right:2px;top:2px;width:16px;height:16px;background:#a78bfa;border-radius:50%}
.preview{background:#000;border-radius:16px;aspect-ratio:16/9;display:grid;place-items:center;border:1px solid #2a2540;position:relative;overflow:hidden}
.stat{background:#1a1630;border:1px solid #2a2540;border-radius:16px;padding:16px;text-align:center}
.score{font-size:32px;font-weight:900;color:#a78bfa;border:3px solid #a78bfa;width:70px;height:70px;border-radius:50%;display:grid;place-items:center;margin:10px auto}
.hook{font-size:11px;text-align:left;padding:8px;background:#151122;border-radius:8px;margin-top:8px;display:flex;justify-content:space-between}
.btn{background:linear-gradient(90deg,#8b5cf6,#a78bfa);border:none;width:100%;padding:16px;border-radius:12px;font-weight:900;color:white;cursor:pointer;font-size:14px}
.right{display:grid;gap:16px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:900px){.wrap{grid-template-columns:1fr}.stats{grid-template-columns:1fr}}
</style></head>
<body>
<div class="nav"><a href="/" class="logo"><div class="logo-icon">▶</div>ClipViral.AI</a><div class="menu"><a href="/">← Volver a Home</a><b>Dashboard</b><span>Library</span><span>Analytics</span></div></div>
<div class="wrap">
<div>
<div class="card"><h3>📤 Upload Video</h3><div class="upload">Drag & drop your video here<br><b>MP4, MOV • Max 3GB • 10h+ Videos</b><br><br><small>or click to browse</small></div></div>
<div class="card" style="margin-top:16px"><h3>🖼 Logo Watermark Upload</h3><div class="field"><span>Upload your logo PNG</span><span style="background:#2a2540;padding:4px 8px;border-radius:6px">Browse</span></div><small style="color:#6b6490;font-size:10px">logo_watermark.png • 32KB</small></div>
<div class="card" style="margin-top:16px"><h3>💬 Subtitle Style</h3><small style="color:#8b7fb0">Color Picker for Subtitles</small><div class="colors"><div class="dot" style="background:#facc15"></div><div class="dot active" style="background:#a78bfa"></div><div class="dot" style="background:#f472b6"></div><div class="dot" style="background:#22c55e"></div><div class="dot" style="background:#38bdf8"></div><div class="dot" style="background:#fff"></div></div><div class="field" style="margin-top:12px"><span>Font Style</span><span>Montserrat Bold ▾</span></div><div class="field"><span>Auto Captions</span><div class="toggle"></div></div></div>
</div>
<div class="right">
<div class="card"><h3>Preview Output</h3><div class="preview"><span>This one habit 10x'd my productivity...</span><div style="position:absolute;top:10px;right:10px;background:#a78bfa;font-size:10px;padding:4px 8px;border-radius:20px">LIVE PREVIEW</div></div></div>
<div class="stats">
<div class="stat"><small>Viral Score</small><div class="score">92%</div><small style="color:#8b7fb0">High potential • Trending Hook</small></div>
<div class="stat" style="text-align:left"><small>Hook Titles</small>
<div class="hook"><span>• This 1 Mistake is Killing Your Views</span><span style="color:#a78bfa">Score 95</span></div>
<div class="hook"><span>• How I Gained 1M in 30 Days! Detail</span><span style="color:#a78bfa">Score 91</span></div>
<div class="hook"><span>• Stop Doing This in Your First 5 Seconds</span><span style="color:#a78bfa">Score 89</span></div>
</div></div>
<button class="btn">✨ Generate Clips Now</button>
<small style="text-align:center;color:#6b6490;display:block">Estimated 5 clips • 30s each • ~5min processing</small>
</div>
</div>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(LANDING)

@app.route("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
