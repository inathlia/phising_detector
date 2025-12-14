import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from imblearn.ensemble import BalancedRandomForestClassifier
from datasets import load_datasets
from features import extract_features

texts, labels = load_datasets()

# Extract features
print("Extracting features...")
X = np.array(
    [extract_features(t) for t in texts],
    dtype=np.float32
)

y = np.array(labels, dtype=np.int8)

# Split data with validation set
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train,
    y_train,
    test_size=0.15,
    stratify=y_train,
    random_state=42
)

# Create pipeline with scaling
# pipeline = Pipeline([
#     ('scaler', StandardScaler()),
#     ('classifier', GradientBoostingClassifier(
#         n_estimators=500,
#         learning_rate=0.05,
#         max_depth=7,
#         min_samples_split=10,
#         min_samples_leaf=4,
#         subsample=0.8,
#         random_state=42,
#         validation_fraction=0.15,
#         n_iter_no_change=20,
#         verbose=1
#     ))
# ])

# Alternative: Balanced Random Forest (uncomment to try)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', BalancedRandomForestClassifier(
        n_estimators=500,
        max_depth=30,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        bootstrap=True,
        n_jobs=-1,
        random_state=42,
        verbose=1
    ))
])

print("Training model...")
pipeline.fit(X_train, y_train)

# Evaluate on validation set
print("\n=== Validation Set Results ===")
val_pred = pipeline.predict(X_val)
print(classification_report(y_val, val_pred, target_names=["Legitimate", "Phishing"]))
print("\nConfusion Matrix:")
print(confusion_matrix(y_val, val_pred))

# Evaluate on test set
print("\n=== Test Set Results ===")
test_pred = pipeline.predict(X_test)
print(classification_report(y_test, test_pred, target_names=["Legitimate", "Phishing"]))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, test_pred))

# Feature importance (if available)
if hasattr(pipeline.named_steps['classifier'], 'feature_importances_'):
    importances = pipeline.named_steps['classifier'].feature_importances_
    top_indices = np.argsort(importances)[-10:][::-1]
    print("\nTop 10 Most Important Features:")
    for idx in top_indices:
        print(f"  Feature {idx}: {importances[idx]:.4f}")

# Save model
with open("backend/model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("\nModel saved to backend/model.pkl")
