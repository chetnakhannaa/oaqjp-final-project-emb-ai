"""Flask web application for Watson NLP emotion detection."""

from flask import Flask, jsonify, render_template, request

from .emotion_detection import EmotionServiceError, emotion_detector


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/emotionDetector")
    def detect_emotion():
        data = request.get_json(silent=True) or {}
        text_to_analyze = data.get("textToAnalyze", request.form.get("textToAnalyze", ""))
        if not text_to_analyze.strip():
            message = "Please enter text to analyze."
            if request.is_json:
                return jsonify({"error": message}), 400
            return message, 400

        try:
            result = emotion_detector(text_to_analyze)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except EmotionServiceError as exc:
            app.logger.exception("Emotion service request failed")
            return jsonify({"error": str(exc)}), 502

        summary = ", ".join(f"{name}: {result[name]:.3f}" for name in ("anger", "disgust", "fear", "joy", "sadness"))
        summary += f"; dominant emotion: {result['dominant_emotion']}"
        if request.is_json:
            return jsonify({"emotions": result, "summary": summary})
        return summary

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
