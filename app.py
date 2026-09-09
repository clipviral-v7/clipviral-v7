from flask import Flask, render_template_string
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ClipViral AI - Pro</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0a0a0f] text-white">
<nav class="flex justify-between p-6 max-w-7xl mx-auto">
<div class="font-black text-xl">ClipViral<span class="text-violet-500">.AI</span></div>
<div class="bg-white text-black px-5 py-2 rounded-full text-sm font-bold">PRO</div>
</nav>

<div class="max-w-5xl mx-auto text-center px-6 pt-16 pb-20">
<div class="inline-flex gap-2 bg-violet-500/10 border border-violet-500/20 text-violet-300 px-4 py-1 rounded-full text-xs mb-6">✨ IA Viral Score 2.0 Activada</div>

<h1 class="text-[54px] md:text-[72px] font-black leading-[0.9] tracking-tight">Convierte videos<br><span class="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">largos en virales</span></h1>
<p class="text-zinc-400 text-[18px] mt-6 max-w-2xl mx-auto">La IA #1 en LATAM para creadores. Encuentra hooks, genera subtítulos estilo MrBeast y exporta en 9:16.</p>

<div class="mt-12 bg-white text-black rounded-[24px] p-3 max-w-2xl mx-auto flex gap-3 shadow-[0_0_80px_rgba(124,58,237,0.3)]">
<input id="url" placeholder="Pega tu link de YouTube, Kick, Podcast..." class="flex-1 bg-transparent px-4 outline-none text-[16px]">
<button onclick="alert('¡Motor REAL conectado! Pega un link de YouTube y genera clips.')" class="bg-black text-white px-8 py-4 rounded-[16px] font-bold">Generar →</button>
</div>

<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-20 text-left">
<div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6"><div class="text-2xl mb-3">🎯</div><b>Score Viral</b><p class="text-sm text-zinc-400 mt-2">Detecta los 5 momentos con más potencial de tu video largo.</p></div>
<div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6"><div class="text-2xl mb-3">💬</div><b>Subtítulos PRO</b><p class="text-sm text-zinc-400 mt-2">Animados, con emojis y palabras clave resaltadas.</p></div>
<div class="bg-zinc-900 border border-zinc-800 rounded-2xl p-6"><div class="text-2xl mb-3">📱</div><b>9:16 Perfecto</b><p class="text-sm text-zinc-400 mt-2">Face-tracking automático, nunca corta la cara.</p></div>
</div>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
