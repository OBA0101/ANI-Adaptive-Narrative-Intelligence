from flask import Flask, render_template, request, jsonify
from narrative_engine import NarrativeEngine


app = Flask(__name__)

# Create the narrative engine
engine = NarrativeEngine()

# Store the current user's story session
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

    # Save the session
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

    # Keep the updated session
    session = result["session"]

    response = {
        "success": True,
        "story": result["story"],
        "tone": result["tone"],
        "choices": result["choices"],
        "completed": result.get("completed", False),
        "state": result["session"]["state"]
    }

    # Include journey summary when the story is complete
    if result.get("completed", False):

        response["summary"] = engine.get_journey_summary(
            session
        )

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