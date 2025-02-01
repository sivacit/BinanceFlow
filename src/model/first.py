import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch
import numpy as np
import os


import mlflow
from mlflow.models import infer_signature

import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# os.environ["MLFLOW_TRACKING_USERNAME"] = "mlflow_user"
# os.environ["MLFLOW_TRACKING_PASSWORD"] = "MLflowP@ssw0rd"
# os.environ["AWS_ACCESS_KEY_ID"] = "bTFjjZKX7zii4LmRs4GW"
# os.environ["AWS_SECRET_ACCESS_KEY"] = "PlOM8wT64lZxGIebtN9pZ6rQPpTluW7uda5AvQzZ"
# os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"

# print("MLflow Tracking URI:", mlflow.get_tracking_uri())
# print("MLflow Artifact Storage:", os.getenv("MLFLOW_S3_ENDPOINT_URL"))
# print("AWS Access Key:", os.getenv("AWS_ACCESS_KEY_ID"))
# print("AWS Secret Key:", os.getenv("AWS_SECRET_ACCESS_KEY"))

# Set MLflow tracking server
mlflow.set_tracking_uri("http://localhost:5001")


# Load the Iris dataset
X, y = datasets.load_iris(return_X_y=True)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define the model hyperparameters
params = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "multi_class": "auto",
    "random_state": 8888,
}

# Train the model
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)

# Set our tracking server uri for logging
mlflow.set_tracking_uri(uri="http://127.0.0.1:5001")

# Create a new MLflow Experiment
mlflow.set_experiment("MLflow Quickstart")

# Start an MLflow run
with mlflow.start_run():
    # Log the hyperparameters
    mlflow.log_params(params)

    # Log the loss metric
    mlflow.log_metric("accuracy", accuracy)

    # Set a tag that we can use to remind ourselves what this run was for
    mlflow.set_tag("Training Info", "Basic LR model for iris data")

    # Infer the model signature
    signature = infer_signature(X_train, lr.predict(X_train))

    # Log the model
    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="tracking-quickstart",
    )