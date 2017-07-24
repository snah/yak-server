#! /usr/bin/env python3

# pylint: disable = no-self-use

import time
import usb

import test.util # noqa

import yak_server.usbdevice


TIMEOUT = 0.1


class TestSwitchInterfaceProtocol(test.util.TestCase):
    def test_button_press_and_release(self):
        device = self._get_device()
        device.connect()

        try:
            while device._endpoint.read(1):
                pass
        except usb.core.USBError:
            pass

        print('Press and hold the button on the test jig.')

        button_down_response = device.read(1)

        self.assertEqual(button_down_response, b'\x01')

        try:
            while device._endpoint.read(1):
                self.fail('Unexpected data received.')
        except usb.core.USBError:
            pass

        print('Release the button on the test jig.')

        button_up_response = device.read(1)

        self.assertEqual(button_up_response, b'\x00')

    def _get_device(self):
        devices = self._find_devices()
        if not devices:
            print('Please plugin the device.')
        while not devices:
            time.sleep(0.1)
            devices = self._find_devices()
        return devices[0]

    @staticmethod
    def _find_devices():
        return yak_server.usbdevice.find(vendor_id=0x04d8, product_id=0x5900)
