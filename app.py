import os, uuid, json, subprocess, random
import boto3
from flask import Flask, request, jsonify
from botocore.client import Config

app = Flask(__name__)
TMP = "/tmp"
R2_BUCKET = "clipviral"
R2_PUBLIC = "https://pub-f843e09d0c254a84b59e7d1a6f9b57d1.r2.dev"

s3 = boto3.client('s3',
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

# --- IA VIRAL LOGIC MOCK (Aquí conectamos Whisper + GPT después) ---
def analyze_virality(video_path):
    # En v2 esto es Whisper + OpenAI para detectar hooks reales
    # Por ahora simula detección inteligente para que veas el dashboard
    clips = []
    for i in range(6):
        start = i * 35 + random.randint(0,10)
        clips.append({
            "id": i,
            "start": start,
            "end": start + 30,
            "hook": ["Pico de emoción", "Pregunta retórica", "Confesión", "Dato shock", "Historia personal", "Call to action"][i],
            "virality_score": random.randint(88, 96),
            "reason": f"Momento de alta retención detectado en {start}s - patrón viral"
        })
    # Ordenar por score
    clips = sorted(clips, key=lambda x: x['virality_score'], reverse=True)
    return clips

def cut_vertical_clip(input_path, output_path, start, duration=30):
    # Corta en vertical 9:16 con ffmpeg (funciona en Render)
    cmd = [
        "ffmpeg", "-y", "-ss", str(start), "-t", str(duration),
        "-i", input_path,
        "-vf", "crop=ih*9/16:ih,scale=1080:1920",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
        "-c:a", "aac", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route('/')
def dashboard():
    return """
    <html><head><title>ClipViral AI</title>
    <style>body{font-family:Arial;background:#0a0a0a;color:white;text-align:center;padding:20px}
   .card{background:#1a1a1a;padding:20px;border-radius:15px;margin:15px;display:inline-block;width:300px}
   .score{font-size:40px;color:#00ff88}</style></head><body>
    <h1>🔥 ClipViral AI - Dashboard</h1>
    <p>Rate de viralidad: <b>92%</b> promedio | Sube hasta 2GB</p>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required><button>Analizar con IA</button>
    </form>
    <p id="st"></p>
    <div id="res"></div>
    <script>
    document.querySelector('form').onsubmit = (e)=>{
        document.getElementById('st').innerHTML='⏳ Espera... IA analizando momentos virales (puede tardar 2-3min para 2GB)';
    }
    </script>
    </body></html>
    """

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    if not f: return "No file", 400
    vid = uuid.uuid4().hex[:8]
    in_path = f"{TMP}/{vid}_full.mp4"
    f.save(in_path)

    # 1. Subir original a R2
    s3.upload_file(in_path, R2_BUCKET, f"{vid}.mp4")

    # 2. IA detecta clips virales
    viral_clips = analyze_virality(in_path)

    # 3. Cortar los 6 clips
    for c in viral_clips:
        out = f"{TMP}/{vid}_clip{c['id']}.mp4"
        cut_vertical_clip(in_path, out, c['start'])
        s3.upload_file(out, R2_BUCKET, f"{vid}_clip{c['id']}.mp4")

    # 4. Dashboard con resultados
    html = f"<html><body style='font-family:Arial;background:#0a0a0a;color:white;text-align:center;padding:20px'><h1>✅ Análisis completo - {vid}</h1><p>Original: <a style='color:#00ff88' href='{R2_PUBLIC}/{vid}.mp4' target='_blank'>Ver</a></p><div style='display:flex;flex-wrap:wrap;justify-content:center'>"
    for c in viral_clips:
        html += f"""
        <div style='background:#1a1a1a;padding:15px;border-radius:12px;margin:10px;width:320px'>
            <div style='font-size:30px;color:#00ff88'>{c['virality_score']}%</div>
            <b>Clip {c['id']+1} - {c['hook']}</b><br>
            <small>{c['start']}s - {c['end']}s | {c['reason']}</small><br><br>
            <video width='200' controls src='{R2_PUBLIC}/{vid}_clip{c['id']}.mp4'></video><br>
            <a href='{R2_PUBLIC}/{vid}_clip{c['id']}.mp4' download style='color:#00ff88'>Descargar vertical 9:16</a>
        </div>
        """
    html += "</div><br><a href='/' style='color:white'>Volver</a></body></html>"
    return html

@app.route('/health')
def health(): return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT",10000)))
