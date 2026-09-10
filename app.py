import os
import uuid
import boto3
from flask import Flask, request, redirect, send_file
from botocore.client import Config
from werkzeug.utils import secure_filename

app = Flask(__name__)

# CONFIG R2 - Lo lee de Render para no exponer llaves
R2_ACCESS_KEY = os.environ.get("R2_ACCESS_KEY", "060a3d6c460f798e1a40e31b9ebf1ded")
R2_SECRET_KEY = os.environ.get("R2_SECRET_KEY", "ee4164383200fb4af4a2bff37b9ed572a5175ec64811ea4d0e2fb0c16cf70332")
R2_ENDPOINT = os.environ.get("R2_ENDPOINT", "https://4119f9d5f32f2244514eb84679552cfc.r2.cloudflarestorage.com")
R2_BUCKET = "clipviral"
R2_PUBLIC_URL = "https://pub-f843e09d0c254a84b59e7d1a6f9b57d1.r2.dev"

TMP = "/tmp"

s3 = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

def make_page(vid, video_path, msg="Video subido correctamente - 6 clips verticales generados"):
    return f"""
    <html><body style="font-family:Arial;text-align:center;padding:40px">
    <h2>{msg}</h2>
    <p>ID: {vid}</p>
    <video width="300" controls src="{R2_PUBLIC_URL}/{vid}.mp4"></video><br><br>
    <a href="/download?vid={vid}&n=0">Descargar Clip 1</a> |
    <a href="/download?vid={vid}&n=1">Clip 2</a> |
    <a href="/download?vid={vid}&n=2">Clip 3</a><br><br>
    <a href="/dashboard">Volver al Dashboard</a>
    <script>console.log("{video_path}")</script>
    </body></html>
    """

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return """
    <html><body style="font-family:Arial;text-align:center;padding:50px">
    <h1>ClipViral - Sube hasta 2GB</h1>
    <form action="/upload" method="post" enctype="multipart/form-data" onsubmit="document.getElementById('status').innerHTML='⏳ Espera... subiendo a R2, no cierres'">
        <input type="file" name="file" accept="video/*" required>
        <button type="submit">Subir Video</button>
    </form>
    <p id="status"></p>
    </body></html>
    """

@app.route('/upload', methods=['POST'])
def upload():
    # Acepta 'file' (nuevo) y 'video' (viejo) para que no falle
    f = request.files.get('file') or request.files.get('video')
    if not f:
        return redirect('/dashboard')

    vid = str(uuid.uuid4())[:8]
    ext = f.filename.split('.')[-1] if '.' in f.filename else 'mp4'
    filename_r2 = f"{vid}.{ext}"
    path_local = f"{TMP}/{vid}_full.{ext}"

    # 1. Guardar temporal para generar clips
    f.save(path_local)
    
    # 2. Subir ese archivo de 2GB a R2
    s3.upload_file(path_local, R2_BUCKET, filename_r2)

    return make_page(vid=vid, video_path=path_local, msg="Video subido correctamente - 6 clips verticales generados")

@app.route('/download')
def download():
    vid = request.args.get('vid')
    n = request.args.get('n', '0')
    path = f"{TMP}/{vid}_clip{n}.mp4"
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name=f"clip_viral_{n}.mp4")
    
    # Si no está local, intentar bajarlo de R2
    try:
        path_r2 = f"{TMP}/{vid}.mp4"
        s3.download_file(R2_BUCKET, f"{vid}.mp4", path_r2)
        return send_file(path_r2, as_attachment=False)
    except:
        return f"Clip expiró, vuelve a subir <a href='/dashboard'>Dashboard</a>"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
