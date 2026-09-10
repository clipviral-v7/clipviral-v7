"""Clipping API: análisis de transcripciones para encontrar momentos compartibles."""
import json
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

ROOT = Path(__file__).parent
app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # Límite seguro para la primera versión.


@app.get("/")
def landing():
    return send_from_directory(ROOT, "index.html")


@app.get("/dashboard")
def dashboard():
    return send_from_directory(ROOT, "dashboard.html")


@app.get("/<path:filename>")
def assets(filename):
    return send_from_directory(ROOT, filename)


@app.post("/api/analyze")
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
"""Clipping API: análisis de transcripciones para encontrar momentos compartibles."""
import json
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI

ROOT = Path(__file__).parent
app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # Límite seguro para la primera versión.


@app.get("/")
def landing():
    return send_from_directory(ROOT, "index.html")


@app.get("/dashboard")
def dashboard():
    return send_from_directory(ROOT, "dashboard.html")


@app.get("/<path:filename>")
def assets(filename):
    return send_from_directory(ROOT, filename)


@app.post("/api/analyze")
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
