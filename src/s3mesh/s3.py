from s3mesh.mesh import MeshMessage
from s3mesh.monitoring.event.forward import ForwardMessageEvent


class S3Uploader:
    def __init__(self, s3_client, bucket_name: str):
        self._s3_client = s3_client
        self._bucket_name = bucket_name

    def upload(self, message: MeshMessage, observation: ForwardMessageEvent):
        s3_file_name = message.file_name.replace(" ", "_")
        key = f"{message.date_delivered.strftime('%Y/%m/%d')}/{s3_file_name}"
        self._s3_client.upload_fileobj(message, self._bucket_name, key)
        observation.record_s3_key(key)
