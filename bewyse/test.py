import json
import os
from cryptography.hazmat.primitives import serialization

# Get the current directory as the base directory
base_dir = os.getcwd() + "bewyse"

# Specify the file name
filename = "bewyse.json"

# Construct the full file path
file_path = os.path.join(base_dir, filename)
print(file_path)

# Check if the file exists
if os.path.exists(file_path):
    # Load the service account key JSON file
    with open(file_path, "r") as f:
        service_account_key_data = json.load(f)

    # Extract the public key in PEM format
    private_key_pem = service_account_key_data['private_key']
    private_key_bytes = private_key_pem.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)

    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode('utf-8')

    print(public_key)
else:
    print(f"File '{filename}' not found in the current directory: {base_dir}")
