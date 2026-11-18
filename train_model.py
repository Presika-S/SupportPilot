
import os
import re
import pickle
import shutil
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# 1. Text cleaning
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(
        r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b",
        " ",
        text
    )
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    patterns = [
        r"\bdear\s+(sir|madam|team|all|colleague)\b",
        r"\bkind regards\b",
        r"\bbest regards\b",
        r"\bthanks and regards\b",
        r"\bthank you and regards\b",
        r"\byours sincerely\b",
        r"\byours faithfully\b"
    ]

    for pattern in patterns:
        text = re.sub(pattern, " ", text)

    return re.sub(r"\s+", " ", text).strip()


# 2. Load dataset
print("\nLoading dataset...")

df = pd.read_csv("processed_tickets.csv")
df = df.dropna(subset=["Document", "Topic_group"]).copy()

X = df["Document"].apply(clean_text)
y = df["Topic_group"].astype(str).str.strip()

valid = X.str.len() > 0
X = X[valid]
y = y[valid]

print("Total records:", len(X))
print("\nCategory distribution:")
print(y.value_counts())


# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 4. Word and character TF-IDF
features = FeatureUnion([
    ("word", TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=15000,
        min_df=2,
        sublinear_tf=True
    )),
    ("char", TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        max_features=10000,
        min_df=2,
        sublinear_tf=True
    ))
])


# 5. Linear SVM pipeline
pipeline = Pipeline([
    ("features", features),
    ("classifier", LinearSVC())
])


# 6. Hyperparameter tuning
parameters = {
    "classifier__C": [0.25, 0.5, 1, 2, 4]
}

grid_search = GridSearchCV(
    pipeline,
    parameters,
    cv=3,
    scoring="accuracy",
    n_jobs=-1,
    verbose=1
)

print("\nTraining SupportPilot Linear SVM model...")
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_


# 7. Evaluation
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n================================")
print("SUPPORTPILOT LINEAR SVM RESULTS")
print("================================")

print("Best parameters:", grid_search.best_params_)

print(
    "Cross-validation accuracy:",
    round(grid_search.best_score_ * 100, 2), "%"
)

print(
    "Test accuracy:",
    round(accuracy * 100, 2), "%"
)

print("\nClassification report:")
print(classification_report(y_test, y_pred))

print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))


# 8. Save only if better than current model
MODEL_PATH = "models/ticket_classifier.pkl"
BASELINE_ACCURACY = 0.8679

os.makedirs("models", exist_ok=True)

if accuracy > BASELINE_ACCURACY:

    if os.path.exists(MODEL_PATH):
        shutil.copy2(
            MODEL_PATH,
            "models/ticket_classifier_backup.pkl"
        )

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)

    print("\nImproved Linear SVM model saved!")

else:
    print("\nNo improvement.")
    print("Existing Logistic Regression model preserved.")

print("\nTraining completed!")
