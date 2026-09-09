from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ClipViral AI - Convierte videos largos en clips virales</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #ffffff; color: #111; }
nav { display:flex; justify-content:space-between; padding:18px 6%; border-bottom:1px solid #eee; align-items:center; }
.logo { font-weight:800; font-size:22px; }
.btn-black { background:#111; color:white; padding:10px 18px; border-radius:8px; text-decoration:none; font-size:14px; }
.hero { max-width:900px; margin:0 auto; text-align:center; padding:80px 20px 40px; }
.hero h1 { font-size:52px; line-height:1.05; letter-spacing:-2px; }
.hero h1 span { background: linear-gradient(90deg,#7c3aed,#ec4899); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero p { color:#666; font-size:19px; margin-top:18px; }
.box { background:white; border:1px solid #e5e7eb; box-shadow: 0 10px 40px rgba(0,0,0,0.08); border-radius:20px; padding:28px; margin:40px auto 0; max-width:640px; }
input { width:100%; padding:18px; border-radius:12px; border:1px solid #ddd; font-size:16px; background:#f9fafb; }
button.main { width:100%; margin-top:14px; padding:18px; border-radius:12px; border:none; background:#111; color:white; font-size:16px; font-weight:600; cursor:pointer; }
.features { display:grid; grid-template-columns: repeat(3,1fr); gap:16px; max-width:900px; margin:60px auto; padding:0 20px; }
.feat { background:#f9fafb; border-radius:16px; padding:20px; text-align:left; }
.feat h3 { font-size:15px; margin-bottom:6px; }
.feat p { font-size:13px; color:#666; margin:0; }
@media(max-width:700px){ .hero h1{font-size:36px;} .features{grid-template-columns:1fr;} }
</style>
</head>
<body>
<nav>
<div class="logo">ClipViral AI</div>
<a class="btn-black" href="#">Iniciar Sesión</a>
</nav>

<div class="hero">
<h1>Convierte videos largos en <span>clips virales</span> en 1 click con IA</h1>
<p>Nuestra IA encuentra los momentos más virales, añade subtítulos animados y los deja listos para TikTok, Reels y Shorts.</p>

<div class="box">
<input id="link" placeholder="Pega aquí el link de YouTube, Podcast, Kick...">
<button class="main" onclick="document.getElementById('result').style.display='block'">Generar Clips Virales →</button>
<div id="result" style="display:none; margin-top:18px; text-align:left; background:#f0fdf4; border:1px solid #bbf7d0; padding:14px; border-radius:10px; font-size:14px;">
✅ <b>IA Analizando...</b><br>En la versión completa aquí tu IA creará 5-10 clips con score viral, subtítulos y formato 9:16 automáticamente.
</div>
<p style="font-size:12px; color:#999; margin-top:12px;">Gratis • Sin marca de agua • Exporta en 1080p</p>
</div>
</div>

<div class="features">
<div class="feat"><h3>🎯 IA Viral Score</h3><p>Detecta ganchos, emociones y momentos con potencial millonario.</p></div>
<div class="feat"><h3>💬 Subtítulos Animados</h3><p>Estilo Hormozi / MrBeast automático en español.</p></div>
<div class="feat"><h3>📱 Reframe 9:16 Auto</h3><p>Centra la cara y crea clips perfectos para TikTok.</p></div>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run()
