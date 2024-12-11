import os
import sys
import yaml
import zipfile
import shutil
from object_detection.utils.main_utils import read_yaml_file
from object_detection.logger import logging
from object_detection.exception import AppException
from object_detection.entity.config_entity import ModelTrainerConfig
from object_detection.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")
            
            # Use zipfile to extract the contents of the zip file
            with zipfile.ZipFile("data.zip", 'r') as zip_ref:
                zip_ref.extractall(".")  # Extract all to the current directory

            # Remove the zip file after extraction
            os.remove("data.zip")

            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            print(model_config_file_name)

            # Read the existing model config and modify it
            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = int(num_classes)

            # Write the modified config to a new file
            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            # Run the training script using Python subprocess or os.system
            os.system(f"cd yolov5/ && python train.py --img 416 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_epochs} --data ../data.yaml --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results  --cache")

            # Copy the best.pt file using shutil
            shutil.copy("yolov5/runs/train/yolov5s_results/weights/best.pt", "yolov5/")

            # Create target directory if it doesn't exist
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)

            # Copy the best.pt file to the model trainer directory
            shutil.copy("yolov5/runs/train/yolov5s_results/weights/best.pt", f"{self.model_trainer_config.model_trainer_dir}/")

            # Clean up by removing unnecessary files and directories
            os.remove("data.yaml")
            shutil.rmtree("yolov5/runs")
            shutil.rmtree("train")
            shutil.rmtree("valid")

            # Create and return the ModelTrainerArtifact with the trained model path
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise AppException(e, sys)
