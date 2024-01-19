import time
from pathlib import Path
import shutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
import logging
from fileType import FileType


class CustomEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"Received creation event - {event.src_path}")
        if not event.is_directory:
            file_path = Path(event.src_path)

            # to make sure the file is actually the correct one and not a temp
            if not file_path.suffix in ['.crdownload', '.tmp', '.part','.pdf.crdownload'] or not file_path.name.startswith('.'):
                # Wait for a short period to ensure it is the correct file, not a temp
                time.sleep(5) 
                try: 
                    if file_path.exists():  # Check if the file still exists after the delay
                        logging.info(f'File downloaded: {file_path}')
                        destination_directory = FileType.return_type(file_path)
                        #destination_directory = Path('/Users/noahjaskiewicz/Desktop/python_demos') - for debugging
                        destination_directory.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file_path), str(destination_directory / file_path.name))
                        logging.info(f"Sucessfully moved {file_path.name} to {destination_directory}")
                except Exception as e:
                    logging.error(f"Error moving file {file_path}: {e}")



