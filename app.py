from flask import Flask, render_template, request, jsonify, session
from narrative_engine import NarrativeEngine

app = Flask(__name__)

app.secret_key = "ani-development-secret-key"

engine = NarrativeEngine()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# START STORY
# ============================================================

@app.route("/start-story", methods=["POST"])
def start_story():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    emotion = data.get("emotion", "").strip()

    if not emotion:
        return jsonify({
            "success": False,
            "message": "Emotion is required."
        }), 400

    story_session = engine.start_story(emotion)

    if story_session is None:
        return jsonify({
            "success": False,
            "message": "Emotion not recognized."
        }), 400

    # Save the session
    session["story_session"] = story_session["session"]

    return jsonify({
        "success": True,
        "story": story_session["story"],
        "tone": story_session["tone"],
        "choices": story_session["choices"],
        "state": story_session["session"]["state"],
        "stage": story_session["session"]["stage"],
        "emotion": story_session["session"]["emotion"]
    })


# ============================================================
# CONTINUE STORY
# ============================================================

@app.route("/continue-story", methods=["POST"])
def continue_story():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    choice = data.get("choice", "").strip()

    if not choice:
        return jsonify({
            "success": False,
            "message": "Choice is required."
        }), 400

    story_session = session.get("story_session")

    if not story_session:
        return jsonify({
            "success": False,
            "message": "No active story session."
        }), 400

    result = engine.adapt_story(
        story_session,
        choice
    )

    if result is None:
        return jsonify({
            "success": False,
            "message": "Unable to continue the story."
        }), 400

    # Save updated session
    session["story_session"] = result["session"]

    return jsonify({
        "success": True,
        "story": result["story"],
        "tone": result["tone"],
        "choices": result["choices"],
        "state": result["session"]["state"],
        "stage": result["session"]["stage"],
        "emotion": result["session"]["emotion"],
        "completed": result.get("completed", False)
    })


# ============================================================
# GET CURRENT NARRATIVE STATE
# ============================================================

@app.route("/story-state", methods=["GET"])
def story_state():

    story_session = session.get("story_session")

    if not story_session:
        return jsonify({
            "success": False,
            "message": "No active story session."
        }), 404

    return jsonify({
        "success": True,
        "emotion": story_session["emotion"],
        "stage": story_session["stage"],
        "state": story_session["state"],
        "choices": story_session["choices"]
    })


# ============================================================
# RESET STORY
# ============================================================

@app.route("/reset-story", methods=["POST"])
def reset_story():

    session.pop("story_session", None)

    return jsonify({
        "success": True,
        "message": "Story session reset."
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "system": "Adaptive Narrative Intelligence",
        "engine": "NarrativeEngine"
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)