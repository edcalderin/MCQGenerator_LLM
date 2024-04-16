import logging
from datetime import datetime
from pathlib import Path
import os

def get_logger():
    LOG_FILE: str = f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log"

    log_path = Path(os.getcwd()).joinpath("logs")

    log_path.mkdir(exist_ok=True) 

    LOGFILE_PATH = log_path.joinpath(LOG_FILE)
    try:
        
        level = logging.INFO
        logger = logging.getLogger()
        logger.setLevel(level)
        
        file_handler = logging.FileHandler(LOGFILE_PATH)
        file_handler.setLevel(level)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        
        formatter = logging.Formatter("[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
            
    except Exception:
        logger = None
    finally:
        return logger
