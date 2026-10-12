# Emotion Detector

A small Flask web app that sends text to an IBM Watson NLP `EmotionPredict` service and reports scores for anger, disgust, fear, joy, and sadness, plus the dominant emotion.

## Requirements

- Python 3.10 or newer
- Network access to your Watson NLP service
- The Watson emotion endpoint URL supplied by your course or deployment

## Setup and run

From this directory, create and activate a virtual environment, then install the package:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
$env:WATSON_EMOTION_URL = "https://YOUR-WATSON-ENDPOINT/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
python -m emotion_detector.app
```

Open <http://127.0.0.1:5000>. The application uses the IBM Watson NLP request header `grpc-metadata-mm-model-id: emotion_aggregated-workflow_lang_en_stock`. If your lab gives you a different endpoint or model ID, change `DEFAULT_URL` or the header in `emotion_detector/emotion_detection.py`.

## API

- `GET /` serves the browser interface.
- `GET /health` returns `{"status":"ok"}`.
- `POST /emotionDetector` accepts form data named `textToAnalyze`; JSON clients may send `{"textToAnalyze":"..."}`. JSON responses contain an `emotions` object and a formatted `summary`.

The service helper returns the five numeric emotion scores and `dominant_emotion`. Invalid input receives HTTP 400; upstream service failures receive HTTP 502.

## Tests and static analysis

```powershell
python -m unittest discover -s tests -v
pylint emotion_detector tests
```

## Build a distributable package

```powershell
python -m pip install build
python -m build
```

The wheel and source archive will be created under `dist/`.
