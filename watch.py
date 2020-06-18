import sys
import time
import os
import uuid
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from WatchEvent import MyHandler


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = PollingObserver()
    print('Start watching ', args[0])
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
