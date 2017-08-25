from yakserver import usbdevice
from tests.doubles.fake_usb_device import FakeUsbDeviceBase


class FakeACDeviceV0_0_0(FakeUsbDeviceBase):
    DEVICE_CLASS_ID = usbdevice.DeviceClassID(vendor_id=0x04d8,
                                              product_id=0x5901,
                                              release_number=0x0001)

    def __init__(self):
        super().__init__()
        self.channel_state = False

    def write(self, data):
        if data == b'\x01':
            self.channel_state = True
        else:
            self.channel_state = False
