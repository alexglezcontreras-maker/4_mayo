"""
Servidor de traducción Alemán ↔ Español con Qwen2-0.5B-Instruct
Mundial 2026 — Alemania vs Curazao

Cómo correr:
  1. pip install flask flask-cors transformers torch
  2. python translator_server.py
  3. Abre translator_app.html en tu navegador

El modelo se descarga automáticamente de HuggingFace (~1 GB) la primera vez.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

app = Flask(__name__)
CORS(app)  # Permite que el HTML llame al servidor

# ── Configuración del modelo ─────────────────────────────────────────────────
MODEL_ID   = "Qwen/Qwen2-0.5B-Instruct"
DEVICE     = "cuda" if torch.cuda.is_available() else "cpu"
MAX_TOKENS = 256

print(f"[INFO] Usando dispositivo: {DEVICE}")
print(f"[INFO] Cargando modelo {MODEL_ID} ...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model     = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map="auto" if DEVICE == "cuda" else None,
)
if DEVICE == "cpu":
    model = model.to(DEVICE)

model.eval()
print("[INFO] Modelo listo ✓")


# ── Función de traducción ────────────────────────────────────────────────────
def translate(text: str, direction: str) -> str:
    """
    direction: "de_es"  (Alemán → Español)
               "es_de"  (Español → Alemán)
    """
    if direction == "de_es":
        sys_prompt = (
            "Eres un traductor experto. Traduce el texto del alemán al español. "
            "Responde ÚNICAMENTE con la traducción, sin explicaciones ni texto adicional."
        )
        user_msg = f"Traduce del alemán al español:\n{text}"
    else:
        sys_prompt = (
            "Du bist ein Expertenübersetzer. Übersetze den Text vom Spanischen ins Deutsche. "
            "Antworte NUR mit der Übersetzung, ohne Erklärungen oder zusätzlichen Text."
        )
        user_msg = f"Übersetze vom Spanischen ins Deutsche:\n{text}"

    messages = [
        {"role": "system",  "content": sys_prompt},
        {"role": "user",    "content": user_msg},
    ]

    # Aplicar chat template de Qwen2
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_TOKENS,
            do_sample=False,            # Greedy – más determinista
            temperature=1.0,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Extraer solo los tokens generados (sin el prompt)
    generated_ids = outputs[0][inputs["input_ids"].shape[-1]:]
    result = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    return result


# ── Endpoints ────────────────────────────────────────────────────────────────
@app.route("/translate", methods=["POST"])
def translate_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    text      = data.get("text", "").strip()
    direction = data.get("direction", "de_es")

    if not text:
        return jsonify({"error": "Campo 'text' vacío"}), 400
    if direction not in ("de_es", "es_de"):
        return jsonify({"error": "direction debe ser 'de_es' o 'es_de'"}), 400

    try:
        translation = translate(text, direction)
        return jsonify({"translation": translation, "direction": direction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": MODEL_ID, "device": DEVICE})


# ── Arranque ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[INFO] Servidor iniciando en http://localhost:5001")
    print("[INFO] Abre translator_app.html en tu navegador")
    print("[INFO] NOTA Mac: AirPlay ocupa el 5000, usamos el 5001")
    app.run(host="0.0.0.0", port=5001, debug=False)
