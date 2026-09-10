import os
import boto3
from flask import Flask, request, jsonify, render_template_string
from botocore.client import Config
from werkzeug.utils import secure_filename

app = Flask(__name__)

# CONFIG R2 - Ya está con tus datos
R2_ACCESS_KEY = "060a3d6c460f798e1a40e31b9ebf1ded"
R2_SECRET_KEY = "ee4164383200fb4af4a2bff37b9ed572a5175ec64811ea4d0e2fb0c16cf70332"
R2_ENDPOINT = "https://4119f9d5f32f2244514eb84679552cfc.r2.cloudflarestorage.com"
R2_BUCKET = "clipviral"
R2_PUBLIC_URL = "https://pub-f843e09d0c254a84b59e7d1a6f9b57d1.r2.dev"

s3 = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name='auto'
)

HTML = """
<!DOCTYPE html>
<html>
<head><title>ClipViral - 2GB</title></head>
<body style="font-family:Arial; text-align:center; padding:50px">
<h1>ClipViral Subida 2GB</h1>
<input type="file" id="file" />
<button onclick="upload()">Subir</button>
<p id="status"></p>
<script>
async function upload(){
  const file = document.getElementById('file').files[0];
  if(!file) return alert('Elige video');
  const status = document.getElementById('status');
  status.innerHTML = `⏳ Espera... 0MB / ${Math.round(file.size/1024/1024)}MB`;

  const form = new FormData();
  form.append('file', file);

  const xhr = new XMLHttpRequest();
  xhr.upload.onprogress = (e) => {
    if(e.lengthComputable){
      let loaded = Math.round(e.loaded/1024/1024);
      let total = Math.round(e.total/1024/1024);
      status.innerHTML = `⏳ Espera... ${loaded}MB / ${total}MB`;
    }
  };
  xhr.onload = () => {
    if(xhr.status==200){
      let res = JSON.parse(xhr.response);
      status.innerHTML = `✅ Exitoso<br><a href="${res.url}" target="_blank">${res.url}</a><br><video width="300" controls src="${res.url}"></video>`;
    } else {
      status.innerHTML = '❌ Error: ' + xhr.response;
    }
  };
  xhr.open('POST', '/upload');
  xhr.send(form);
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    filename = secure_filename(f.filename)
    # Subir directo a R2
    s3.upload_fileobj(f, R2_BUCKET, filename)
    url = f"{R2_PUBLIC_URL}/{filename}"
    return jsonify({"url": url, "status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
