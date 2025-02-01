import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # Correct MinIO endpoint
    aws_access_key_id="root",
    aws_secret_access_key="password"
)

s3.upload_file("train.py", "mlflow", "train.py")
print("Upload successful!")