import os
import abc
from google.cloud import storage as gcs


GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")


class ObjectStorageRepository(abc.ABC):

    def load_contents(self, bucket: str, key: str) -> str:
        raise NotImplementedError()


class GcsRepository(ObjectStorageRepository):

    def __init__(self, project_id: str) -> None:
        super().__init__()
        self.__project_id = project_id
        self.__client = gcs.Client(project=self.__project_id)
        self.__buckets = {}


    def load_contents(self, bucketName: str, key: str) -> str:

        bucket = self.__get_bucket(bucketName)

        blob = bucket.blob(key)

        return blob.download_as_text()

    def __init_bucket(self, bucket) -> None:
        self.__buckets[bucket] = self.__client.get_bucket(bucket)

    def __get_bucket(self, bucketName: str) -> gcs.Bucket:
        bucket = self.__buckets.get(bucketName)
        if not bucket:
            self.__init_bucket(bucket)
            bucket = self.__buckets[bucket]

        return bucket


def create_object_storage_repository(project_id: str = GCP_PROJECT_ID) -> ObjectStorageRepository:
    return GcsRepository(project_id=project_id)
