from flask import Flask, render_template, request, jsonify, session
from narrative_engine import NarrativeEngine

app = Flask(__name__)

# Required for Flask sessions
app.secret_key = "ani-development-secret-key"

engine = NarrativeEngine()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_story():

    data = request.get_json()

    emotion = data.get("emotion")

    result = engine.start_story(emotion)

    if result is None:
        return jsonify({
            "success": False,
            "error": "Invalid emotion selected."
        }), 400

    # Store the narrative session
    session["story_session"] = result["session"]

    return jsonify({
        "success": True,
        "story": result["story"],
        "tone": result["tone"],
        "choices": result["choices"]
    })


@app.route("/choose", methods=["POST"])
def choose():

    data = request.get_json()

    choice = data.get("choice")

    story_session = session.get("story_session")

    if not story_session:
        return jsonify({
            "success": False,
            "error": "No active story session."
        }), 400

    result = engine.adapt_story(
        story_session,
        choice
    )

    if result is None:
        return jsonify({
            "success": False,
            "error": "Unable to process choice."
        }), 400

    # Save updated session
    session["story_session"] = result["session"]

    response = {
        "success": True,
        "story": result["story"],
        "tone": result["tone"],
        "choices": result["choices"],
        "completed": result.get("completed", False)
    }

    # If the story has finished, include the journey summary
    if result.get("completed", False):

        summary = engine.get_journey_summary(
            result["session"]
        )

        response["summary"] = summary

    return jsonify(response)


@app.route("/journey-summary", methods=["GET"])
def journey_summary():

    story_session = session.get("story_session")

    if not story_session:
        return jsonify({
            "success": False,
            "error": "No journey found."
        }), 404

    summary = engine.get_journey_summary(
        story_session
    )

    return jsonify({
        "success": True,
        "summary": summary
    })


if __name__ == "__main__":
    app.run(debug=True)