import os, re, joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "complaint_classifier.joblib")

PREFIX = re.compile(r"^(urgent:|complaint:|hi team,|good morning,|hello,|dear sir,|sir,|"
                    r"please help,|respected sir/madam,|i would like to complain that|"
                    r"i request you to look into this:)\s*")
SUFFIX = re.compile(r"\s*(please help\.?|thank you\.?|kindly look into it\.?|this is very urgent\.?|"
                    r"it is affecting my studies\.?|please resolve this soon\.?|please take action\.?|"
                    r"request you to solve it as soon as possible\.?|yaar|"
                    r"i have complained before but nothing happened\.?)$")


def clean(t):
    t = t.lower().strip()
    prev = None
    while prev != t:
        prev = t
        t = PREFIX.sub("", t)
        t = SUFFIX.sub("", t).strip()
    return t


_model = None


def _load():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(text):
    """Returns (category, confidence). Confidence is None if the model can't give one."""
    model = _load()
    cleaned = clean(text)
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([cleaned])[0]
        i = probs.argmax()
        return str(model.classes_[i]), float(probs[i])
    return str(model.predict([cleaned])[0]), None