from flask import Flask, render_template_string, request, send_file
import os, uuid, yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)
TMP = "/tmp/clips"
os.makedirs(TMP, exist_ok=True)

HTML_BASE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ClipViral AI</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap'); body{font-family:'Inter',sans-serif}</style>
</head>
<body class="bg-[#fcfcfc] text-zinc-900">
<nav class="flex justify-between items-center px-[6%] py-5 bg-white border-b"><div class="font-black text-[22px]">ClipViral AI</div><a class="bg-black text-white px-4 py-2 rounded-lg text-sm">Iniciar Sesión</a></nav>
<div class="max-w-[900px] mx-auto text-center px-5 pt-[70px]">
<h1 class="text-[52px] leading-[1.05] tracking-[-2px] font-black">Convierte vídeos largos en <span class="bg-gradient-to-r from-violet-600 to-pink-500 bg-clip-text text-transparent">clips virales</span> en 1 click con IA</h1>
<p class="text-[#666] text-[19px] mt-5 max-w-[650px] mx-auto">Nuestra IA encuentra los momentos más virales, añade subtítulos animados y los deja listos para TikTok, Reels y Shorts.</p>
<div class="bg-white border border-zinc-200 shadow-[0_20px_60px_rgba(0,0,0,0.08)] rounded-[20px] p-7 mt-10 max-w-[640px] mx-auto text-left">
<form action="/generate" method="POST">
<input name="url" required placeholder="Pega aquí el link de YouTube, Kick..." class="w-full p-[18px] rounded-xl border border-zinc-200 bg-[#f9fafb] text-[16px] outline-none">
<button class="w-full mt-4 p-[18px] rounded-xl bg-black text-white font-semibold text-[16px]">Generar Clips Virales →</button>
</form>
<p class="text-[12px] text-zinc-400 text-center mt-3">Gratis • Sin marca de agua • Exporta en 1080p</p>
</div>
<div class="grid md:grid-cols-3 gap-4 max-w-[900px] mx-auto mt-16 text-left pb-20">
<div class="bg-[#f9fafb] rounded-2xl p-5 border"><b class="text-[15px]">🎯 IA Viral Score</b><p class="text-[13px] text-zinc-500 mt-1">Detecta ganchos y momentos millonarios.</p></div>
<div class="bg-[#f9fafb] rounded-2xl p-5 border"><b class="text-[15px]">💬 Subtítulos Animados</b><p class="text-[13px] text-zinc-500 mt-1">Estilo Hormozi automático.</p></div>
<div class="bg-[#f9fafb] rounded-2xl p-5 border"><b class="text-[15px]">📱 Reframe 9:16 Auto</b><p class="text-[13px] text-zinc-500 mt-1">Centra la cara perfectamente.</p></div>
</div>
</div>
</body></html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_BASE)

@app.route("/generate", methods=["POST"])
def generate():
    url = request.form.get("url","")
    job = str(uuid.uuid4())[:6]
    full = os.path.join(TMP, f"{job}_full.mp4")
    try:
        ydl_opts = {'outtmpl': full, 'format': 'best[height<=720]', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Error: {e} <br><a href='/'>Volver</a>"

    return f"✅ Video descargado correctamente! Ahora implementamos el corte. Tamaño: {os.path.getsize(full)} bytes <br><a href='/'>Volver</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
