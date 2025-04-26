from datasets import load_dataset
from azure.storage.blob import BlobServiceClient
import os
import json  # To handle JSON serialization
import time
with open('local.settings.json', 'r') as f:
    config = json.load(f)
# Azure Function App Configuration

# Azure Blob Storage Configuration
STORAGE_CONNECTION_STRING =  config.get("Values", {}).get("AzureWebJobsmaqpocearningcalls_STORAGE", "")
CONTAINER_NAME = "input-transcripts"  # Replace with the name of your container
BLOB_NAME = "earnings_call_row.json"  # Replace with the desired name for your blob

# Hugging Face Dataset Configuration
DATASET_NAME = 'jlh-ibm/earnings_call'
ROW_INDEX = 0  # Change this to the index of the row you want to store
DATASET_SPLIT = 'train'  # Specify the split you want to use (e.g., 'train', 'test')
NUM_ROWS_TO_UPLOAD = 10  # Number of rows to upload (adjust as needed)

def upload_rows_to_azure_blob(dataset_name, dataset_split, num_rows, storage_connection_string, container_name):
    """
    Loads rows from a Hugging Face dataset and uploads each row as a separate .txt (or .json)
    file to Azure Blob Storage.

    Args:
        dataset_name (str): The name of the Hugging Face dataset.
        dataset_split (str): The dataset split to use (e.g., 'train', 'test').
        num_rows (int): The number of rows to upload.
        storage_connection_string (str): The Azure Blob Storage connection string.
        container_name (str): The name of the Azure Blob Storage container.
    """

    try:
        # 1. Load the dataset
        dataset = load_dataset(dataset_name, split=dataset_split)

        # 2. Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # 3. Iterate through rows and upload each as a separate blob
        for i in range(min(num_rows, len(dataset))):  # Process up to num_rows or dataset length
            row_data = dataset[i]

            # Choose how to format the data and name the blob
            # Option A: JSON (more structured)
            # blob_content = json.dumps(row_data, indent=2, ensure_ascii=False)
            # blob_name = f"row_{i}.txt"

            # Option B: Text (if you only want the 'raw_text' or similar)
            blob_content = row_data.get('text', '')  # Adjust 'raw_text' if needed
            blob_name = f"row_{i}.txt"

            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(blob_content, overwrite=True)

            print(f"Row {i} uploaded to Azure Blob Storage as '{blob_name}' in container '{container_name}'.")
            # Set a delay to simulate real-time processing
            time.sleep(10) # Adjust the delay in seconds as needed

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_rows_to_azure_blob(DATASET_NAME, DATASET_SPLIT, NUM_ROWS_TO_UPLOAD, STORAGE_CONNECTION_STRING, CONTAINER_NAME)