from flask import Flask, render_template_string, request, redirect, session
import os
app = Flask(__name__)
app.secret_key = "clipviral_v7_secreto"
CREDITOS = {"eduardo": 10}
GALERIA = [
    {"streamer": "Westcol", "titulo": "Westcol se enoja con la casa", "views": "1.2M", "thumb": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"},
    {"streamer": "Westcol", "titulo": "La mejor reacción del stream", "views": "890K", "thumb": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"},
]
LANDING_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-black text-white"><div class="min-h-screen flex flex-col items-center justify-center p-6 text-center"><h1 class="text-5xl font-black mb-4">Deja de editar 6 horas.<br><span class="text-purple-500">Nuestra IA clipea a Westcol por ti mientras duermes</span></h1><p class="text-xl text-gray-400 mt-4 mb-8">Pega el link, nosotros clipeamos, tú cobras.</p><a href="/login" class="bg-purple-600 px-8 py-4 rounded-full font-bold text-xl">Empezar a Farmear →</a></div></body></html>"""
DASHBOARD_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-zinc-900 text-white p-6"><div class="max-w-5xl mx-auto"><div class="flex justify-between items-center mb-8"><h1 class="text-2xl font-bold">Panel de Clipper</h1><div class="bg-zinc-800 px-4 py-2 rounded-full">Creditos: {{creditos}} ⚡</div></div><div class="grid grid-cols-1 md:grid-cols-2 gap-6"><div class="bg-zinc-800 p-6 rounded-xl"><h2 class="font-bold mb-4">1. Farmear Streamer</h2><input placeholder="Pega link de Kick/Twitch/Youtube" class="w-full p-3 rounded bg-zinc-700 mb-3"><button onclick="alert('¡Clip generado! -1 credito')" class="w-full bg-purple-600 p-3 rounded font-bold">Generar Clips (1 credito)</button></div><div class="bg-zinc-800 p-6 rounded-xl"><h2 class="font-bold mb-4">2. Conectar TikTok</h2><button class="w-full bg-white text-black p-3 rounded font-bold">Conectar TikTok @tu_cuenta</button></div></div><h2 class="text-xl font-bold mt-10 mb-4">Galería Pública</h2><div class="grid grid-cols-2 md:grid-cols-3 gap-4">{% for clip in galeria %}<div class="bg-zinc-800 rounded-xl overflow-hidden"><img src="{{clip.thumb}}"><div class="p-3"><p class="font-bold text-sm">{{clip.titulo}}</p><p class="text-xs text-gray-400">{{clip.streamer}} · {{clip.views}}</p></div></div>{% endfor %}</div></div></body></html>"""
@app.route("/")
def landing(): return render_template_string(LANDING_HTML)
@app.route("/login")
def login():
    session["user"] = "eduardo"
    return redirect("/dashboard")
@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect("/")
    return render_template_string(DASHBOARD_HTML, creditos=CREDITOS["eduardo"], galeria=GALERIA)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
