from pathlib import Path
from services.processor import process_features
from services.extractor import extract_vector
from services.extractor import extract_features

def predict_apk(apk_path: Path, model, feature_names=None):
    raw_features = extract_features(apk_path)
    X = process_features(raw_features, feature_names)

    if model.n_features_in_ != X.shape[1]:
        raise ValueError("Feature count differs from training.")

    if hasattr(model, "feature_names_in_"):
        if list(model.feature_names_in_) != X.columns.tolist():
            raise ValueError("Feature order differs from training.")

    print("predictions:", model.predict(X))

    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    print("Prediction:", prediction, "Probability:", max(probabilities))
   
    return {
        "predicted_label": (
            prediction.item()
            if hasattr(prediction, "item")
            else prediction
        ),
        "class_probabilities": {
            str(label): float(probability)
            for label, probability in zip(
                model.classes_, probabilities
            )
        },
    }