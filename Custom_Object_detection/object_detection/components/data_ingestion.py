import os
import sys
import zipfile
import gdown
import time
from object_detection.logger import logging
from object_detection.exception import AppException
from object_detection.entity.config_entity import DataIngestionConfig
from object_detection.entity.artifacts_entity import DataIngestionArtifact



def download_with_retries(download_url, zip_file_path, retries=3, delay=5):
    for attempt in range(retries):
        try:
            gdown.download(download_url, zip_file_path, quiet=False)
            return True
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise AppException("Failed to download file after multiple attempts", sys)



class DataIngestion:
    def __init__(self,data_url, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        self.data_url=data_url
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
           raise AppException(e, sys)
       
       
       


        
    '''def download_data(self)-> str:


        try: 
            dataset_url = self.data_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = "data.zip"
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")


            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix+file_id,zip_file_path)

            logging.info(f"Downloaded data from {dataset_url} into file {zip_file_path}")

            return zip_file_path

        except Exception as e:
            raise AppException(e, sys)'''
            
    def download_data(self) -> str:
        try:
            dataset_url = self.data_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = "data.zip"
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            download_url = f"{prefix}{file_id}"

            download_with_retries(download_url, zip_file_path)

            logging.info(f"Downloaded data from {dataset_url} into file {zip_file_path}")
            return zip_file_path

        except Exception as e:
            raise AppException(e, sys)
        

    
    def extract_zip_file(self,zip_file_path: str)-> str:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}")

            return feature_store_path

        except Exception as e:
            raise AppException(e, sys)
        


    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path = zip_file_path,
                feature_store_path = feature_store_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise AppException(e, sys)
        
        
        

    
    
        