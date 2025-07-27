import pandas as pd
import argparse
import mlflow
import mlflow.sklearn
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from mlflow.models.signature import infer_signature
import os

def load_data(path):
    return pd.read_csv(path)

def preprocess(df):
    df.drop(columns=['Id'], inplace=True)
    le = LabelEncoder()
    df['Species'] = le.fit_transform(df['Species'])
    return df, le

def train_and_log_model(model, model_name, X_train, X_test, y_train, y_test):
    with mlflow.start_run(run_name=model_name):
        model.fit(X_train, y_train)

        # Training metrics
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        y_prob_train = model.predict_proba(X_train)

        mlflow.log_param("model_type", model_name)
        mlflow.log_metric("training_accuracy_score", accuracy_score(y_train, y_pred_train))
        mlflow.log_metric("training_precision_score", precision_score(y_train, y_pred_train, average='macro'))
        mlflow.log_metric("training_recall_score", recall_score(y_train, y_pred_train, average='macro'))
        mlflow.log_metric("training_f1_score", f1_score(y_train, y_pred_train, average='macro'))
        mlflow.log_metric("training_log_loss", log_loss(y_train, y_prob_train))
        mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred_test))

        # Register and save model
        signature = infer_signature(X_train, model.predict(X_train))
        if model_name == "RandomForest":
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                registered_model_name="iris_randomforest_model",
                signature=signature
            )
            joblib.dump(model, 'app/model.pkl')  # Save only the final selected model
        else:
            mlflow.sklearn.log_model(model, "model")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/Iris.csv", help="Path to input dataset")
    args = parser.parse_args()

    # Load and preprocess data
    df = load_data(args.input)
    df, label_encoder = preprocess(df)

    # Save LabelEncoder for decoding in API
    os.makedirs("app", exist_ok=True)
    joblib.dump(label_encoder, 'app/label_encoder.pkl')

    # Prepare features and target
    X = df.drop("Species", axis=1)
    y = df["Species"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Logistic Regression
    logreg = LogisticRegression(max_iter=200)
    train_and_log_model(logreg, "LogisticRegression", X_train, X_test, y_train, y_test)

    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    train_and_log_model(rf, "RandomForest", X_train, X_test, y_train, y_test)
