"""Clipping API: análisis de transcripciones para encontrar momentos compartibles."""
import json
import os
import sqlite3
import tempfile
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template_string, request, send_from_directory, session, url_for
from openai import OpenAI
from werkzeug.security import check_password_hash, generate_password_hash

ROOT = Path(__file__).parent
app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "replace-this-secret-in-render")
DATABASE = ROOT / "users.db"


def db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with db() as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)")


@app.before_request
def ensure_database():
    init_db()


def login_required(api=False):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return (jsonify(error="Debes iniciar sesión."), 401) if api else redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped
    return decorator


@app.get("/")
def landing():
    return send_from_directory(ROOT, "index.html")


AUTH_PAGE = """<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{{ title }} | Clipping</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#f6f5f1;font-family:Arial;color:#151519}.box{width:min(390px,calc(100% - 40px));padding:32px;background:#fff;border:1px solid #dfddd7;border-radius:16px}.brand{font-size:23px;font-weight:800;text-decoration:none;color:#151519}.brand b{color:#7855ff}h1{font-size:28px;margin:30px 0 8px}.sub{color:#6e6b72;font-size:14px;line-height:1.5}label{display:block;font-size:12px;font-weight:bold;margin:17px 0 6px}input{box-sizing:border-box;width:100%;padding:12px;border:1px solid #d6d4cf;border-radius:8px;font-size:14px}button{width:100%;margin-top:22px;border:0;border-radius:8px;padding:13px;background:#7855ff;color:#fff;font-size:14px;font-weight:bold}.error{padding:10px;background:#fff0ed;color:#a13c2d;border-radius:7px;font-size:13px}.switch{text-align:center;color:#6e6b72;font-size:13px;margin:20px 0 0}.switch a{color:#6442d8;font-weight:bold;text-decoration:none}</style></head><body><main class='box'><a class='brand' href='/'>clipp<b>•</b>ing</a><h1>{{ title }}</h1><p class='sub'>{{ subtitle }}</p>{% if error %}<p class='error'>{{ error }}</p>{% endif %}<form method='post'><label>Correo electrónico</label><input name='email' type='email' required autocomplete='email'><label>Contraseña</label><input name='password' type='password' required minlength='8' autocomplete='{{ autocomplete }}'><button>{{ action }}</button></form><p class='switch'>{{ switch_text }} <a href='{{ switch_url }}'>{{ switch_link }}</a></p></main></body></html>"""


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email, password = request.form.get("email", "").strip().lower(), request.form.get("password", "")
        if len(password) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
        else:
            try:
                with db() as connection:
                    cursor = connection.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, generate_password_hash(password)))
                session["user_id"] = cursor.lastrowid
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                error = "Ya existe una cuenta con ese correo."
    return render_template_string(AUTH_PAGE, title="Crea tu cuenta", subtitle="Regístrate para probar Clipping.", action="Crear cuenta", switch_text="¿Ya tienes una cuenta?", switch_url=url_for("login"), switch_link="Inicia sesión", autocomplete="new-password", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        with db() as connection:
            user = connection.execute("SELECT * FROM users WHERE email = ?", (request.form.get("email", "").strip().lower(),)).fetchone()
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        error = "Correo o contraseña incorrectos."
    return render_template_string(AUTH_PAGE, title="Bienvenido", subtitle="Inicia sesión para abrir tu estudio.", action="Iniciar sesión", switch_text="¿No tienes cuenta?", switch_url=url_for("register"), switch_link="Regístrate gratis", autocomplete="current-password", error=error)


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.get("/dashboard")
@login_required()
def dashboard():
    return send_from_directory(ROOT, "dashboard.html")


@app.get("/<path:filename>")
def assets(filename):
    if filename == "dashboard.html" and "user_id" not in session:
        return redirect(url_for("login"))
    return send_from_directory(ROOT, filename)


@app.post("/api/analyze")
@login_required(api=True)
def analyze():
    """Transcribe el vídeo y devuelve tres cortes sugeridos con sus timestamps."""
    if not os.getenv("OPENAI_API_KEY"):
        return jsonify(error="Falta configurar OPENAI_API_KEY en Render."), 503
    uploaded = request.files.get("video")
    if not uploaded or not uploaded.filename:
        return jsonify(error="Envía un vídeo en el campo 'video'."), 400

    suffix = Path(uploaded.filename).suffix or ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        uploaded.save(tmp.name)
        temp_path = tmp.name

    try:
        client = OpenAI()
        # whisper-1 entrega segmentos con timestamps, indispensables para cortar el vídeo.
        with open(temp_path, "rb") as media:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=media,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
                language="es",
            )
        segments = [
            {"start": round(s.start, 1), "end": round(s.end, 1), "text": s.text}
            for s in (transcript.segments or [])
        ]
        prompt = """Eres editor experto de clips virales para streamers hispanos.
Analiza los segmentos con timestamps. Propón exactamente 3 clips de 15 a 55 segundos,
sin inventar tiempos fuera de los segmentos. Prioriza sorpresa, humor, conflicto,
reacción, logro, frases contundentes o conversación que genere comentarios.
Devuelve SOLAMENTE JSON válido con esta forma:
{"clips":[{"start":12.0,"end":35.0,"score":86,"title":"texto corto","reason":"por qué puede funcionar"}]}.
Puntuación 0-100: es una estimación, no una garantía de viralidad.
SEGMENTOS:\n""" + json.dumps(segments, ensure_ascii=False)
        result = client.responses.create(model="gpt-4.1-mini", input=prompt)
        raw = result.output_text.strip().replace("```json", "").replace("```", "").strip()
        clips = json.loads(raw).get("clips", [])
        return jsonify(clips=clips, transcript=transcript.text)
    except json.JSONDecodeError:
        return jsonify(error="La IA devolvió un formato inesperado; prueba de nuevo."), 502
    except Exception as exc:
        app.logger.exception("Analysis failed")
        return jsonify(error=f"No se pudo analizar el vídeo: {str(exc)}"), 502
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            pass


@app.errorhandler(413)
def too_large(_error):
    return jsonify(error="El archivo supera 25 MB. Para streams grandes hay que añadir subida directa a almacenamiento."), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))

