from flask import Flask, render_template, request, jsonify
from narrative_engine import NarrativeEngine


app = Flask(__name__)

# ============================================================
# ANI NARRATIVE ENGINE
# ============================================================

engine = NarrativeEngine()

# Current active journey
session = None


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# START STORY
# ============================================================

@app.route("/start", methods=["POST"])
def start_story():

    global session

    data = request.get_json()

    if not data or "emotion" not in data:
        return jsonify({
            "success": False,
            "error": "No emotion was provided."
        }), 400

    emotion = data["emotion"]

    result = engine.start_story(emotion)

    if result is None:
        return jsonify({
            "success": False,
            "error": "Invalid emotion."
        }), 400

    # Store the active journey
    session = result["session"]

    return jsonify({
        "success": True,
        "story": result["story"],
        "tone": result["tone"],
        "choices": result["choices"],
        "state": result["session"]["state"]
    })


# ============================================================
# MAKE A CHOICE
# ============================================================

@app.route("/choose", methods=["POST"])
def choose():

    global session

    if session is None:
        return jsonify({
            "success": False,
            "error": "No active story session."
        }), 400

    data = request.get_json()

    if not data or "choice" not in data:
        return jsonify({
            "success": False,
            "error": "No choice was provided."
        }), 400

    choice = data["choice"]

    result = engine.adapt_story(
        session,
        choice
    )

    if result is None:
        return jsonify({
            "success": False,
            "error": "Unable to process the choice."
        }), 400

    # Store the updated journey
    session = result["session"]

    response = {
        "success": True,
        "story": result["story"],
        "tone": result["tone"],
        "choices": result["choices"],
        "completed": result.get("completed", False),
        "state": result["session"]["state"]
    }

    # --------------------------------------------------------
    # JOURNEY COMPLETION
    # --------------------------------------------------------

    if result.get("completed", False):

        summary = engine.get_journey_summary(
            session
        )

        # Add the complete state history
        summary["state_history"] = (
            session["journey_memory"]["state_snapshots"]
        )

        response["summary"] = summary

    return jsonify(response)


# ============================================================
# JOURNEY SUMMARY
# ============================================================

@app.route("/summary", methods=["GET"])
def summary():

    global session

    if session is None:
        return jsonify({
            "success": False,
            "error": "No active story session."
        }), 400

    result = engine.get_journey_summary(
        session
    )

    # --------------------------------------------------------
    # STATE HISTORY
    # --------------------------------------------------------

    result["state_history"] = (
        session["journey_memory"]["state_snapshots"]
    )

    return jsonify({
        "success": True,
        "summary": result
    })


# ============================================================
# RESET JOURNEY
# ============================================================

@app.route("/reset", methods=["POST"])
def reset():

    global session

    session = None

    return jsonify({
        "success": True,
        "message": "Journey reset successfully."
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )