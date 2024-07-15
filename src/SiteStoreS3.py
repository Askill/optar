import json
import os
from pathlib import Path
from typing import List, Optional
import boto3


class SiteStoreS3:
    def __init__(self, bucket):
        self.bucket = bucket

    def get_site_history(self, cache_path) -> Optional[list[str]]:
        # Make sure you provide / in the end
        prefix = cache_path
        if cache_path[-1] != "/":
            prefix += "/"

        s3 = boto3.client("s3")
        result = s3.list_objects_v2(Bucket=self.bucket, Prefix=cache_path, MaxKeys=21)
        if "Contents"not in result:
            return None
        # return a sorted list of file names (key), which are the creation dates, ignore the prefix (len(cache_path)), ignore the first element, as this is only the prefix
        return sorted([x["Key"][len(cache_path) :] for x in result["Contents"][1:]])

    def get_site_links(self, path):
        s3 = boto3.resource('s3')
        obj = s3.Object(self.bucket,path)
        data=obj.get()['Body']
        return json.load(data)

    def persist(self, path, data):
        s3 = boto3.resource('s3')
        s3object = s3.Object(self.bucket, path)
        s3object.put(
            Body=(bytes(json.dumps(data).encode('UTF-8')))
        )