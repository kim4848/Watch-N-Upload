import sys
import time
import os
import uuid
from azure.storage.blob import BlobServiceClient
from watchdog.events import PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.xml", "*.jpg"]
    connect_str = ""

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        print(event.event_type)
        print(event.src_path)
        if event.event_type == 'created':
            self.upload(event.src_path)

    def on_modified(self, event):
        print("on_modified")

    def on_created(self, event):
        self.process(event)

    def upload(self, path):
        blobname = str(uuid.uuid4())+".jpg"
        blob_service_client = BlobServiceClient.from_connection_string(
            self.readConnectionString())
        container_name = "demo"
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blobname)

        tryLoading = True
        while tryLoading:
            try:
                with open(path, "rb") as data:
                    tryLoading = False
                    blob_client.upload_blob(data)
                    data.close()
                break
            except IOError:
                time.sleep(3)

        while True:
            try:
                print("Deleting :"+path)
                os.remove(path)
                print("Deleted")
                break
            except IOError:
                time.sleep(3)

    def readConnectionString(self):
        if len(self.connect_str) > 0:
            return self.connect_str
        else:
            connStr = ""
            with open("./connectionstring.json", "r") as connection:
                connStr = connection.read()
                connection.close()
            self.connect_str = connStr
            return connStr
