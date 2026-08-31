"""
AI Agent Backend - Central Brain
Handles chat (AI conversation), task (automation commands), and memory (context storage)
for both PC and phone apps.
"""

import os
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# ---------- CONFIG ----------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
API_SECRET = os.environ.get("API_SECRET", "changeme")  # simple shared-secret auth for your devices
MODEL_NAME = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ---------- SIMPLE FILE-BASED MEMORY (swap for a real DB later) ----------
MEMORY_FILE = "memory_store.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "facts": {}}


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------- AUTH ----------
def check_auth(req):
    token = req.headers.get("X-API-Key", "")
    return token == API_SECRET


# ---------- ROUTES ----------

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "ai-agent-backend", "time": datetime.utcnow().isoformat()})


@app.route("/chat", methods=["POST"])
def chat():
    if not check_auth(request):
        return jsonify({"error": "unauthorized"}), 401

    if client is None:
        return jsonify({"error": "GROQ_API_KEY not configured on server"}), 500

    body = request.get_json(force=True)
    user_message = body.get("message", "")
    device = body.get("device", "unknown")  # "pc" or "phone"

    if not user_message:
        return jsonify({"error": "message is required"}), 400

    memory = load_memory()

    # Build conversation context from recent history (last 10 turns)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful personal AI agent that assists the user across "
                "their PC and phone. Be concise and practical. If the user asks you "
                "to perform an action (open app, run script, control phone), respond "
                "with a clear plain-language instruction that the client app can act on."
            ),
        }
    ]
    for turn in memory["history"][-10:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Save to memory
    memory["history"].append({"role": "user", "content": user_message, "device": device, "time": time.time()})
    memory["history"].append({"role": "assistant", "content": reply, "device": device, "time": time.time()})
    save_memory(memory)

    return jsonify({"reply": reply})


@app.route("/task", methods=["POST"])
def task():
    """
    Receives an automation command intent (e.g. from voice or text) and returns
    a structured action for the PC or phone app to execute locally.
    The backend itself doesn't execute system actions — it interprets intent
    and returns instructions; the client app performs the actual action.
    """
    if not check_auth(request):
        return jsonify({"error": "unauthorized"}), 401

    if client is None:
        return jsonify({"error": "GROQ_API_KEY not configured on server"}), 500

    body = request.get_json(force=True)
    command = body.get("command", "")
    device = body.get("device", "unknown")

    if not command:
        return jsonify({"error": "command is required"}), 400

    system_prompt = (
        "You convert user automation requests into a strict JSON object describing "
        "the action to take. Only output JSON, nothing else. Schema: "
        '{"action": "open_app|open_url|run_script|search|send_message|unknown", '
        '"target": "string", "params": {}}. '
        "If unsure, use action \"unknown\" and put your best guess in target."
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command},
            ],
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        action = json.loads(raw)
    except Exception as e:
        return jsonify({"error": f"failed to parse action: {str(e)}"}), 500

    memory = load_memory()
    memory["history"].append({
        "role": "user",
        "content": f"[TASK from {device}] {command}",
        "device": device,
        "time": time.time(),
    })
    save_memory(memory)

    return jsonify({"action": action})


@app.route("/memory", methods=["GET"])
def get_memory():
    if not check_auth(request):
        return jsonify({"error": "unauthorized"}), 401
    memory = load_memory()
    return jsonify(memory)


@app.route("/memory/fact", methods=["POST"])
def set_fact():
    """Store a durable fact/preference, e.g. {"key": "wake_word", "value": "Thanos"}"""
    if not check_auth(request):
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json(force=True)
    key = body.get("key")
    value = body.get("value")
    if not key:
        return jsonify({"error": "key is required"}), 400
    memory = load_memory()
    memory["facts"][key] = value
    save_memory(memory)
    return jsonify({"status": "saved", "facts": memory["facts"]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
