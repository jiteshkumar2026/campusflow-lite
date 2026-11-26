import os, re, joblib, pandas as pd
from classifier import clean
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix, f1_score



df = pd.read_csv("complaints.csv")
df["clean"] = df["text"].map(clean)
print(df["category"].value_counts())
print("unique cleaned texts:", df["clean"].nunique(), "of", len(df))

conf = df.groupby("clean")["category"].nunique()
print("conflicting labels:\n", df[df["clean"].isin(conf[conf > 1].index)])

groups = df["clean"].factorize()[0]
X, y = df["clean"], df["category"]

candidates = {
    "tfidf+logreg": Pipeline([("t", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
                              ("c", LogisticRegression(max_iter=2000, class_weight="balanced"))]),
    "tfidf+svm": Pipeline([("t", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
                           ("c", LinearSVC(class_weight="balanced"))]),
    "char-tfidf+logreg": Pipeline([("t", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True)),
                                   ("c", LogisticRegression(max_iter=2000, class_weight="balanced"))]),
}

cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
best, best_f1 = None, 0
for name, m in candidates.items():
    pred = cross_val_predict(m, X, y, groups=groups, cv=cv)
    f1 = f1_score(y, pred, average="macro")
    print(f"\n== {name}  macro-F1 = {f1:.3f}")
    print(classification_report(y, pred))
    if f1 > best_f1:
        best, best_f1 = name, f1

print("Best:", best)
final = candidates[best].fit(X, y)

test = pd.read_csv("test_holdout.csv")
test["clean"] = test["text"].map(clean)
overlap = test["clean"].isin(set(X)).sum()
print("holdout rows overlapping training:", overlap)
test = test[~test["clean"].isin(set(X))]
pred = final.predict(test["clean"])
print(classification_report(test["category"], pred))
print(confusion_matrix(test["category"], pred, labels=sorted(y.unique())))

os.makedirs("models", exist_ok=True)
joblib.dump(final, "models/complaint_classifier.joblib")
print("Model saved.")