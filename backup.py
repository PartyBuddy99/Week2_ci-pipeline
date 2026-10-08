import configparser
import sys
import json
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

def build_key(prefix, today, name):
    return f"{prefix}/{today}/{name}"

def upload_files(s3, folder, bucket, prefix, today):
    uploaded = []
    for name in os.listdir(folder):
        local_path = os.path.join(folder, name)
        if os.path.isfile(local_path):
            key = build_key(prefix, today, name)
            s3.upload_file(local_path, bucket, key)
            uploaded.append(key)
    return uploaded


if __name__ == "__main__":
    with open("config.json") as json_file:
        config = json.load(json_file)

    bucket = config["bucket"]
    folder = config["folder"]
    prefix = config["prefix"]
    today = datetime.today().strftime("%Y%m%d")

    session = boto3.Session(profile_name=config["profile"])
    s3 = session.client("s3")

    try:
        for key in upload_files(s3, folder, bucket, prefix, today):
            print("Uploaded",key)
    except ClientError as e:
        print(e.response["Error"]["Message"])

