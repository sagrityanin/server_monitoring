from ping3 import ping, verbose_ping
from time import sleep
import signal
from contextlib import contextmanager

URL = "e1.ru"


class TimeoutException(Exception): 
    pass


class Ping:
    def __init__(self):
        self.common_time = 0
        self.count = 0
        self.bad_count = 0

    @contextmanager
    def time_limit(self, seconds):
        def signal_handler(signum, frame):
            raise TimeoutException("Timed out!")
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    
    def ping(self, url, i):
        res = ping(url)
        if res := ping(url):
            self.count += 1
            self.common_time += float(res)
        else:
            self.bad_count += 1
        print(f"{i} - {res}")

    def check_ping(self, url: str) -> None:
        for i in range(3600):
            try:
                with self.time_limit(2):
                    self.ping(url, i)
                sleep(1)
            except Exception as e:
                print(f"{i} - {e}")
                self.bad_count += 1
        print(f"Good count = {self.count}")
        print(f"Average time = {self.common_time / self.count}")
        print(f"Bab count = {self.bad_count}")
    

if __name__ == "__main__":
    p = Ping().check_ping(URL)
