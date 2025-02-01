import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch
import numpy as np
import os

os.environ["MLFLOW_TRACKING_USERNAME"] = "mlflow_user"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "MLflowP@ssw0rd"
os.environ["AWS_ACCESS_KEY_ID"] = "bTFjjZKX7zii4LmRs4GW"
os.environ["AWS_SECRET_ACCESS_KEY"] = "PlOM8wT64lZxGIebtN9pZ6rQPpTluW7uda5AvQzZ"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"

print("MLflow Tracking URI:", mlflow.get_tracking_uri())
print("MLflow Artifact Storage:", os.getenv("MLFLOW_S3_ENDPOINT_URL"))
print("AWS Access Key:", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS Secret Key:", os.getenv("AWS_SECRET_ACCESS_KEY"))

# Set MLflow tracking server
mlflow.set_tracking_uri("http://localhost:5001")

# Dummy dataset
X = torch.tensor(np.random.rand(100, 10), dtype=torch.float32)
y = torch.tensor(np.random.randint(0, 2, (100, 1)), dtype=torch.float32)

# Define a simple model
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 1)
    
    def forward(self, x):
        return torch.sigmoid(self.fc(x))

# Training
model = SimpleModel()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Log model with MLflow
with mlflow.start_run():
    for epoch in range(50):
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
    
    mlflow.log_metric("final_loss", loss.item())
    mlflow.pytorch.log_model(model, "pytorch_model")

    run_id = mlflow.active_run().info.run_id
    model_uri = f"runs:/{run_id}/pytorch_model"

    # Register the model
    mlflow.register_model(model_uri, "PytorchModel")

    print("Model URI:", model_uri)
    print("Model registered!")
    print("Run ID:", run_id)