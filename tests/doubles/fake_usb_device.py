import queue


class FakeUsbDeviceBase:
    DEVICE_CLASS_ID = None

    def __init__(self):
        self._read_buffer = b''
        self._read_queue = queue.Queue()

    def connect(self):
        pass

    def flush(self):
        self._read_buffer = b''
        while not self._read_queue.empty():
            self._read_queue.get()

    def read(self, number_of_bytes):
        if len(self._read_buffer) < number_of_bytes:
            self._update_read_buffer()
        return self._get_read_data(number_of_bytes)

    @property
    def class_identifier(self):
        return self.DEVICE_CLASS_ID

    def _update_read_buffer(self):
        self._read_buffer += self._read_queue.get()

    def _get_read_data(self, number_of_bytes):
        response = self._read_buffer[:number_of_bytes]
        self._read_buffer = self._read_buffer[len(response):]
        return response
