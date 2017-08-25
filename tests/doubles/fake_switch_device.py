from yakserver import usbdevice
from tests.doubles.fake_usb_device import FakeUsbDeviceBase


class FakeSwitchDeviceV0_0_1(FakeUsbDeviceBase):
    DEVICE_CLASS_ID = usbdevice.DeviceClassID(vendor_id=0x04d8,
                                              product_id=0x5900,
                                              release_number=0x0001)

    def __init__(self):
        super().__init__()
        self.button_state = [False] * 8

    def press_button(self, button_number):
        self.button_state[button_number - 1] = True
        self._send_button_state()

    def release_button(self, button_number):
        self.button_state[button_number - 1] = False
        self._send_button_state()

    def _send_button_state(self):
        self._read_queue.put(b'\x00' + self._button_data())

    def _button_data(self):
        buttons_down = (i for i, state in enumerate(self.button_state)
                        if state)
        data = sum(2 ** i for i in buttons_down)
        return bytes([data])


class FakeSwitchDeviceV0_0_0(FakeUsbDeviceBase):
    DEVICE_CLASS_ID = usbdevice.DeviceClassID(vendor_id=0x04d8,
                                              product_id=0x5900,
                                              release_number=0x0000)

    def press_button(self):
        self._read_queue.put(b'\x01')

    def release_button(self):
        self._read_queue.put(b'\x00')


class FakeSwitchDevice(FakeSwitchDeviceV0_0_1):
    pass
