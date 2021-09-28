from systemwatch import SystemWatch
import sys
import os

def main():
    sysWatch = SystemWatch(interval=5, ram_threshold=20, cpu_threshold=2)
    sysWatch.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

