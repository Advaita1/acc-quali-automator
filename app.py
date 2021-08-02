from tools.watchers import Watcher
from config import FILE_PATH

if __name__ == '__main__':
    watch = Watcher(FILE_PATH)
    print('Watching for file creation...')
    watch.run()
