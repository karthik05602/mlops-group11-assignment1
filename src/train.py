import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import mlflow
import mlflow.sklearn

# Load dataset
df = pd.read_csv("data/iris.csv")

# Assume the last column is the target if not named
target_col = "Species" if "Species" in df.columns else df.columns[-1]

X = df.drop(columns=[target_col])
y = df[target_col]

# Encode target
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Enable MLflow autologging (optional)
mlflow.sklearn.autolog()

# Experiment setup
mlflow.set_experiment("iris_classification")
best_score = 0
best_model = None
best_run_id = None

models = {
    "LogisticRegression": LogisticRegression(max_iter=200),
    "RandomForest": RandomForestClassifier(n_estimators=100)
}

for name, model in models.items():
    with mlflow.start_run(run_name=name) as run:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, name)

        if acc > best_score:
            best_score = acc
            best_model = model
            best_run_id = run.info.run_id

print(f"Best model logged under run ID: {best_run_id}")