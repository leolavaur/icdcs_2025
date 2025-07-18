"""nslkdd: Utilities for downloading, extracting, and converting the NSL-KDD dataset to Hugging Face format."""

import os
import tempfile
import zipfile
from pathlib import Path

import pandas as pd
import requests
from datasets import ClassLabel, Dataset, DatasetDict, Features, Value

DATASET_URL = "https://github.com/HoaNP/NSL-KDD-DataSet/archive/refs/heads/master.zip"

# Use a persistent user cache directory for all data operations
CACHE_DIR = Path.home() / ".cache" / "nslkdd_data"
DATA_DIR = CACHE_DIR
ZIP_PATH = DATA_DIR / "nslkdd.zip"
EXTRACTED_DIR = DATA_DIR / "NSL-KDD-DataSet-master"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define all features and their types in a single dictionary
FEATURES_SPEC = {
    "duration": Value("int32"),
    "protocol_type": Value("string"),  # names will be set after reading data
    "service": Value("string"),
    "flag": Value("string"),
    "src_bytes": Value("int32"),
    "dst_bytes": Value("int32"),
    "land": Value("int32"),
    "wrong_fragment": Value("int32"),
    "urgent": Value("int32"),
    "hot": Value("int32"),
    "num_failed_logins": Value("int32"),
    "logged_in": Value("int32"),
    "num_compromised": Value("int32"),
    "root_shell": Value("int32"),
    "su_attempted": Value("int32"),
    "num_root": Value("int32"),
    "num_file_creations": Value("int32"),
    "num_shells": Value("int32"),
    "num_access_files": Value("int32"),
    "num_outbound_cmds": Value("int32"),
    "is_host_login": Value("int32"),
    "is_guest_login": Value("int32"),
    "count": Value("int32"),
    "srv_count": Value("int32"),
    "serror_rate": Value("float32"),
    "srv_serror_rate": Value("float32"),
    "rerror_rate": Value("float32"),
    "srv_rerror_rate": Value("float32"),
    "same_srv_rate": Value("float32"),
    "diff_srv_rate": Value("float32"),
    "srv_diff_host_rate": Value("float32"),
    "dst_host_count": Value("int32"),
    "dst_host_srv_count": Value("int32"),
    "dst_host_same_srv_rate": Value("float32"),
    "dst_host_diff_srv_rate": Value("float32"),
    "dst_host_same_src_port_rate": Value("float32"),
    "dst_host_srv_diff_host_rate": Value("float32"),
    "dst_host_serror_rate": Value("float32"),
    "dst_host_srv_serror_rate": Value("float32"),
    "dst_host_rerror_rate": Value("float32"),
    "dst_host_srv_rerror_rate": Value("float32"),
    "label": Value("string"),
    # "difficulty" is only used for reading, not in features
}


def download_dataset():
    """Download the NSL-KDD dataset zip file if not already present."""
    if not ZIP_PATH.exists():
        print("Downloading NSL-KDD dataset...")
        r = requests.get(DATASET_URL)
        with open(ZIP_PATH, "wb") as f:
            f.write(r.content)
    else:
        print("Dataset zip already exists.")


def extract_dataset():
    """Extract the NSL-KDD dataset zip file if not already extracted."""
    if not EXTRACTED_DIR.exists():
        print("Extracting dataset...")
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(DATA_DIR)
    else:
        print("Dataset already extracted.")


def load_df(path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    df = pd.read_csv(path, names=list(FEATURES_SPEC.keys()) + ["difficulty"])
    # Ensure categorical columns are strings and stripped
    for col in ["protocol_type", "service", "flag", "label"]:
        df[col] = df[col].astype(str).str.strip()
    if "difficulty" in df.columns:
        df = df.drop(columns=["difficulty"])
    df["binary_label"] = (df["label"] != "normal").astype("int64")
    return df


def load_nslkdd():
    """Build the full NSL-KDD Hugging Face dataset (train/test) with all features and labels.

    Returns
    -------
    datasets.DatasetDict
        A dictionary with 'train' and 'test' splits as Hugging Face Datasets.
    """
    download_dataset()
    extract_dataset()

    train_df = load_df(EXTRACTED_DIR / "KDDTrain+.txt")
    test_df = load_df(EXTRACTED_DIR / "KDDTest+.txt")

    # Create ClassLabel features for categorical columns
    proto_types = sorted(set(train_df["protocol_type"]).union(test_df["protocol_type"]))
    service_types = sorted(set(train_df["service"]).union(test_df["service"]))
    flag_types = sorted(set(train_df["flag"]).union(test_df["flag"]))
    class_labels = sorted(set(train_df["label"]).union(test_df["label"]))

    features = dict(FEATURES_SPEC)
    features["protocol_type"] = ClassLabel(names=proto_types)
    features["service"] = ClassLabel(names=service_types)
    features["flag"] = ClassLabel(names=flag_types)
    features["label"] = ClassLabel(names=class_labels)
    features["binary_label"] = Value("int32")  # 0 or 1
    features = Features(features)

    # Ensure DataFrame columns match Features keys exactly and reset index
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    train_df = train_df[list(features.keys())]
    test_df = test_df[list(features.keys())]

    train_ds = Dataset.from_pandas(train_df, features=features)
    test_ds = Dataset.from_pandas(test_df, features=features)

    return DatasetDict({"train": train_ds, "test": test_ds})


if __name__ == "__main__":
    ds = load_nslkdd()
    print(ds)
    ds.save_to_disk(str(DATA_DIR / "huggingface_nslkdd"))
    print(f"Hugging Face dataset saved to {DATA_DIR / 'huggingface_nslkdd'}")
