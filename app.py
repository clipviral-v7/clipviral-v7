from flask import Flask, render_template_string
app = Flask(__name__)

HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClipGenius AI - Gradio v4.30</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,system-ui,sans-serif}
body{background:#0e0a1f;color:white}
.nav{background:#151122;display:flex;justify-content:space-between;align-items:center;padding:14px 24px;border-bottom:1px solid #2a2540}
.logo{display:flex;align-items:center;gap:8px;font-weight:900}
.logo-icon{width:28px;height:28px;background:linear-gradient(135deg,#a78bfa,#f472b6);border-radius:8px;display:grid;place-items:center}
.menu{display:flex;gap:20px;color:#8b7fb0;font-size:13px}
.menu b{color:white}
.wrap{display:grid;grid-template-columns:380px 1fr;gap:20px;max-width:1200px;margin:20px auto;padding:0 20px}
.card{background:#1a1630;border:1px solid #2a2540;border-radius:16px;padding:18px}
.card h3{font-size:13px;color:#a89ccf;margin-bottom:12px;display:flex;align-items:center;gap:6px}
.upload{border:1px dashed #3a3560;border-radius:12px;padding:30px;text-align:center;color:#6b6490;font-size:13px;background:#151122}
.upload b{color:#a78bfa}
.field{background:#151122;border:1px solid #2a2540;border-radius:10px;padding:12px;margin-top:10px;display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#8b7fb0}
.colors{display:flex;gap:8px;margin-top:10px}
.dot{width:22px;height:22px;border-radius:50%;border:2px solid #2a2540;cursor:pointer}
.dot.active{border-color:white}
.toggle{width:36px;height:20px;background:#3a3560;border-radius:20px;position:relative}
.toggle::after{content:'';position:absolute;right:2px;top:2px;width:16px;height:16px;background:#a78bfa;border-radius:50%}
.right{display:grid;grid-template-rows:auto auto;gap:16px}
.preview{background:#000;border-radius:16px;aspect-ratio:16/9;display:grid;place-items:center;border:1px solid #2a2540;position:relative;overflow:hidden}
.preview span{color:white;font-size:13px;background:rgba(0,0,0,.6);padding:6px 10px;border-radius:20px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.stat{background:#1a1630;border:1px solid #2a2540;border-radius:16px;padding:16px;text-align:center}
.score{font-size:32px;font-weight:900;color:#a78bfa;border:3px solid #a78bfa;width:70px;height:70px;border-radius:50%;display:grid;place-items:center;margin:10px auto}
.hook{font-size:11px;text-align:left;padding:8px;background:#151122;border-radius:8px;margin-top:8px;display:flex;justify-content:space-between}
.btn{background:linear-gradient(90deg,#8b5cf6,#a78bfa);border:none;width:100%;padding:16px;border-radius:12px;font-weight:900;color:white;cursor:pointer;font-size:14px}
@media(max-width:900px){.wrap{grid-template-columns:1fr}}
</style></head>
<body>
<div class="nav"><div class="logo"><div class="logo-icon">▶</div>ClipGenius <span style="font-weight:400;color:#8b7fb0;font-size:11px">AI Video Clipper • Gradio v4.30</span></div><div class="menu"><b>Dashboard</b><span>Library</span><span>Analytics</span><span>Settings</span></div></div>
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
</div>
</div>
<button class="btn">✨ Generate Clips Now</button>
<small style="text-align:center;color:#6b6490;display:block">Estimated 5 clips • 30s each • ~5min processing</small>
</div>
</div>
</body></html>
"""
@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
