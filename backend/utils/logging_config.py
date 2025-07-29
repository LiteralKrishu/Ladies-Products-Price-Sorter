import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from ..config import Config

def setup_logging():
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                logs_dir / "app.log",
                maxBytes=1024 * 1024 * 5,  # 5MB
                backupCount=3
            ),
            logging.StreamHandler()
        ]
    )
    
    # Set specific log levels for noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)