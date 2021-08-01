from tools.watchers import Watcher
from config import FILE_PATH

if __name__ == '__main__':
    watch = Watcher(FILE_PATH)
    watch.run()