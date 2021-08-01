import time
from watchdog.observers import Observer
from .handlers import Handler

class Watcher:
    def __init__(self, watchDirectory):
        self.observer = Observer()
        self.watchDirectory = watchDirectory

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print('Quali automator has stopped...')

        self.observer.join()
