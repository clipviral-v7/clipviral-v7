from flask import Flask
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipViral AI v3 MORADO</title>
<style>
body{margin:0;background:#08080a;color:#fff;font-family:system-ui,Arial}
.top{display:flex;justify-content:space-between;padding:20px}
.logo{font-weight:900;font-size:20px} .logo i{color:#a855f7;font-style:normal}
.pro{background:#fff;color:#000;padding:8px 14px;border-radius:20px;font-weight:800;font-size:12px}
.wrap{max-width:900px;margin:40px auto;text-align:center;padding:0 20px}
h1{font-size:48px;line-height:.9;font-weight:900;margin:0} 
h1 span{background:linear-gradient(90deg,#a78bfa,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
p.sub{color:#999;margin-top:12px}
.form{background:#fff;border-radius:18px;padding:6px;display:flex;max-width:560px;margin:30px auto}
.form input{flex:1;border:0;padding:0 14px;outline:none;color:#000}
.form button{background:#000;color:#fff;border:0;padding:14px 20px;border-radius:12px;font-weight:800}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:30px;text-align:left}
.box{background:#1a1a1e;border:1px solid #2a2a2e;border-radius:14px;padding:14px}
.box b{font-size:14px} .box p{color:#888;font-size:12px;margin-top:4px}
@media(max-width:600px){.grid{grid-template-columns:1fr} h1{font-size:32px}}
</style></head>
<body>
<div class="top"><div class="logo">ClipViral<i>.AI</i></div><div class="pro">v3 MORADO</div></div>
<div class="wrap">
<h1>Convierte videos<br><span>largos en virales</span></h1>
<p class="sub">La IA #1 en LATAM - Diseño PRO morado activado</p>
<div class="form"><input placeholder="Pega tu link YouTube..."><button>Generar →</button></div>
<div class="grid">
<div class="box"><b>🎯 Score Viral</b><p>Detecta los 5 momentos con más potencial</p></div>
<div class="box"><b>💬 Subtitulos PRO</b><p>Estilo MrBeast animado</p></div>
<div class="box"><b>📱 9:16 Perfecto</b><p>Face-tracking automatico</p></div>
</div>
</div>
</body></html>"""

@app.route("/")
def home():
    return HTML

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
