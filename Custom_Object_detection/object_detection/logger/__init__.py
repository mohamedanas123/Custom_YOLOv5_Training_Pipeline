import logging
import os
from datetime import datetime
from from_root import from_root

log_dir = os.path.join(from_root(), 'log')
os.makedirs(log_dir, exist_ok=True)

log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]

if log_files:
    log_file = log_files[0]  # Use the first existing log file
else:
    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_file_path = os.path.join(log_dir, log_file)

logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
