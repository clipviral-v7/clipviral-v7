from flask import Flask, request
import random
app = Flask(__name__)

HTML_BASE = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;background:#000;color:#fff;font-family:sans-serif}
.nav{padding:20px;font-weight:900;font-size:22px} .nav span{color:#a855f7}
.hero{text-align:center;padding:40px 20px} h1{font-size:48px;font-weight:900;line-height:1.1} h1 span{color:#a855f7}
.box{max-width:650px;margin:30px auto;background:#111;border:1px solid #222;border-radius:20px;padding:24px}
input{width:100%;padding:16px;border-radius:12px;border:1px solid #333;background:#18181b;color:#fff;font-size:14px}
button{width:100%;margin-top:14px;padding:14px;border-radius:999px;background:#a855f7;color:#fff;font-weight:800;border:none;font-size:16px;cursor:pointer}
.clip{max-width:650px;margin:12px auto;background:#111;border:1px solid #222;border-radius:14px;padding:16px;text-align:left}
.rate{background:#a855f7;padding:5px 12px;border-radius:20px;font-weight:900;font-size:13px;color:#fff}
.meta{color:#888;font-size:12px;margin-top:4px}
</style></head><body>
<div class="nav">ClipViral<span>.AI</span></div>
<div class="hero">
<h1>Corta videos largos en <span>clips virales</span> 🚀</h1>
<p style="color:#888;margin-top:12px">YouTube • TikTok • Twitch • Kick</p>
<div class="box">
<form action="/analyze" method="post">
<input type="text" name="url" placeholder="Pega link: youtube.com / tiktok.com / twitch.tv / kick.com" required>
<button type="submit">Analizar con IA ✨</button>
</form>
</div>
</div>
"""

@app.route('/')
def home():
    return HTML_BASE + "</body></html>"

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url','')[:70]
    html = HTML_BASE
    html += f"<p style='text-align:center;color:#555;font-size:12px'>Analizando: {url}</p>"
    for i in range(6):
        score = random.randint(88,99)
        html += f"<div class='clip'><div><span class='rate'>{score}/100</span> <b>Clip #{i+1}</b><div class='meta'>⏱️ 00:{random.randint(10,59)} - 00:{random.randint(60,90)} • Hook viral detectado</div></div></div>"
    html += "<div style='text-align:center;margin:30px'><a href='/' style='color:#a855f7;text-decoration:none'>← Analizar otro</a></div></body></html>"
    return html

@app.route('/health')
def health(): return "OK"
