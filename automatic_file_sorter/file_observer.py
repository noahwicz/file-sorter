import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import logging
from customEventHandler import CustomEventHandler

# HOW TO IMPLEMENT IN TERMINAL WINDOW:
# cd /Users/noahjaskiewicz/Desktop/python_file_project/  - opens the directory to 
# python3 watchdog_demo.py /Users/noahjaskiewicz/Downloads  - sets the file to be monitored to the Downloads Folder


if __name__ == '__main__':


    # Logs the event to a certain display in the command window - currently not used
    #logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(process)d - %(message)s', 
    #                    datefmt='%Y-%m-%d %H:%M:%S')

    #how to store the logs in a file
    logging.basicConfig(filename='dev.log', filemode='a',level=logging.INFO,format='%(asctime)s - %(process)d - %(message)s', 
                       datefmt='%Y-%m-%d %H:%M:%S')



    # Directory or File to be monitored
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(path)
    #event_handler = LoggingEventHandler()  # for logging the event
    event_handler = CustomEventHandler()  # for sending the event to customEventHandler.py
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    #keeps the programming running until an input
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        #print("file recognized")
        observer.stop()
        observer.join()