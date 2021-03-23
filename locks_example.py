import threading
import time
from threading import Lock


# Funktion für die Threads
def do_something(id, duration):
    print(id + " startet ... ", end="")
    time.sleep(duration)
    print(id + " endet\n", end="")


def do_something_with_lock(id, duration):
    with lock:
        print(id + " startet ... ", end="")
        time.sleep(duration)
        print(id + " endet\n", end="")


# Erstelle ein Lock
lock = Lock()

# Serieller Aufruf ----------------------------------------------
do_something("Transaktion 1", 2)
do_something("Transaktion 2", 1)

print("")

# Paralleler Aufruf ohne Lock ------------------------------------
threading.Thread(target=do_something, args=("Transaktion 1", 2)).start()
threading.Thread(target=do_something, args=("Transaktion 2", 1)).start()

time.sleep(3)
print("")

# Paralleler Aufruf ohne Lock ------------------------------------
threading.Thread(target=do_something_with_lock, args=("Transaktion 1", 2)).start()
threading.Thread(target=do_something_with_lock, args=("Transaktion 2", 1)).start()
