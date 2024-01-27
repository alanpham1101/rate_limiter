import csv
import datetime
import os
import threading
import time


class Base:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def _handle(self, *args, **kwargs) -> None:
        pass

    def _forward(self, request, timestamp) -> None:
        pass

    def _drop(self, request, timestamp) -> None:
        pass

    def handle(self, *args, **kwargs) -> None:
        pass


class CSVLog:
    def _generate_file_path(self, file_name) -> None:
        directory = "./logs/"
        if not os.path.isdir(directory):
            os.mkdir(directory)
        return os.path.join(directory, file_name)

    def _write_log(self, file_name, logs) -> None:
        def _generate_log_message(message_logs):
            for message, request, timestamp in message_logs:
                message = f"Request {message}: {request}"
                timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
                yield message, timestamp

        file_path = self._generate_file_path(file_name)
        with open(file_path, "w") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(_generate_log_message(logs))


class TokenBucket(Base, CSVLog):
    def __init__(self, capacity, refill_rate) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.logs = list()

    def _handle(self) -> None:
        """
            Handle function for Token Bucket algorithm
            - Init threads to mimic API calls and rate limiter
                + t1: Rate limiter
                + t2: Request calls
            - Write logs to file

        """
        print('----- START -----')
        t1 = threading.Thread(target=self._run_rate_limiter)
        t2 = threading.Thread(target=self._run_request_call)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        self._write_log(file_name="token_bucket_logs.csv", logs=self.logs)
        print('----- DONE -----')

    def _run_rate_limiter(self) -> None:
        """
            Add n tokens every second
        """
        counter = 0
        while counter < 10:
            time.sleep(1)
            self.tokens += self.refill_rate
            self.tokens = min(self.tokens, self.capacity)
            counter += 1

    def _run_request_call(self) -> None:
        """
            Call requests
            Check:
                - If tokens > 0 -> forward
                - Else -> drop
        """
        request = 0
        while request < 50:
            time.sleep(0.2)
            timestamp = datetime.datetime.now()

            if self.tokens < 1:
                self._drop(request, timestamp)
            else:
                self.tokens -= 1
                self._forward(request, timestamp)
            request += 1

    def _forward(self, request, timestamp) -> None:
        self.logs.append(('Forwarded', request, timestamp))

    def _drop(self, request, timestamp) -> None:
        self.logs.append(('Dropped', request, timestamp))

    def handle(self) -> None:
        self._handle()


class LeakyBucket(Base, CSVLog):
    def __init__(self, capacity, outflow_rate) -> None:
        self.capacity = capacity
        self.outflow_rate = outflow_rate
        self.bucket = list()
        self.logs = list()

    def _handle(self) -> None:
        """
            Handle function for Leaky Bucket algorithm
            - Init threads to mimic API calls and rate limiter
                + t1: Rate limiter
                + t2: Request calls
            - Write logs to file

        """
        print('----- START -----')
        t1 = threading.Thread(target=self._run_rate_limiter)
        t2 = threading.Thread(target=self._run_request_call)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        self._write_log(file_name="leaky_bucket_logs.csv", logs=self.logs)
        print('----- DONE -----')

    def _run_rate_limiter(self) -> None:
        """
            Execute n requests every second
        """
        counter = 0
        while counter < 10:
            time.sleep(1)
            outflow_rate = self.outflow_rate
            while outflow_rate:
                timestamp = datetime.datetime.now()
                if self.bucket:
                    request = self.bucket.pop(0)
                    self._forward(request, timestamp)
                    outflow_rate -= 1
                counter += 1

    def _run_request_call(self) -> None:
        """
            Call requests
            Check:
                - If size(bucket) < capacity -> forward
                - Else -> drop
        """
        request = 0
        while request < 50:
            time.sleep(0.2)
            timestamp = datetime.datetime.now()
            if len(self.bucket) >= self.capacity:
                self._drop(request, timestamp)
            else:
                self.bucket.append(request)
            request += 1

    def _forward(self, request, timestamp) -> None:
        self.logs.append(('Forwarded', request, timestamp))

    def _drop(self, request, timestamp) -> None:
        self.logs.append(('Dropped', request, timestamp))

    def handle(self) -> None:
        self._handle()
