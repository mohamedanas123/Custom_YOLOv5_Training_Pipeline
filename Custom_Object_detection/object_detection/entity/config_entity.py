import os
from dataclasses import dataclass
from datetime import datetime
from object_detection.constant.training_pipeline.config import Config



@dataclass
class TrainingPipelineConfig:
    artifacts_dir: str = Config.ARTIFACTS_DIR



training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig() 


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, Config.DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, Config.DATA_INGESTION_FEATURE_STORE_DIR
    )

    data_download_url: str = Config.DATA_DOWNLOAD_URL



@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, Config.DATA_VALIDATION_DIR_NAME
    )

    valid_status_file_dir: str = os.path.join(data_validation_dir, Config.DATA_VALIDATION_STATUS_FILE)

    required_file_list = Config.DATA_VALIDATION_ALL_REQUIRED_FILES





@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, Config.MODEL_TRAINER_DIR_NAME
    )

    weight_name = Config.MODEL_TRAINER_PRETRAINED_WEIGHT_NAME

    no_epochs = Config.MODEL_TRAINER_NO_EPOCHS

    batch_size = Config.MODEL_TRAINER_BATCH_SIZE


