import json
from watchdog.events import FileSystemEventHandler
from .builders import build_fastest_laps
from .sheet_updaters import update_quali_sheet
from config import SPREADSHEET_NAME

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        """Updates quali sheet on file creation.

        Keyword arguments:
        event -- File system event.
        """
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Open created file
            file = open(event.src_path)
            # Build python dict
            data = json.load(file)
            # Update sheet
            update_quali_sheet(build_fastest_laps(data), SPREADSHEET_NAME)

            file.close()