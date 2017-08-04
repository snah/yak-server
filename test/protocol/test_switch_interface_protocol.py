#! /usr/bin/env python3

# pylint: disable = no-self-use, attribute-defined-outside-init

import time

import test.util # noqa
import test.doubles.fake_switch_device

import yak_server.usbdevice


TIMEOUT = 0.1


class Bases:
    class SwitchInterfaceProtocolTestBase(test.util.TestCase):
        def test_button_press_and_release(self):
            device = self._get_device()
            device.connect()
            device.flush()

            self._press_button()

            button_down_response = device.read(1)
            self.assertEqual(button_down_response, b'\x01')
            device.flush()

            self._release_button()
            button_up_response = device.read(1)
            self.assertEqual(button_up_response, b'\x00')

        def _press_button(self):
            raise NotImplementedError()

        def _release_button(self):
            raise NotImplementedError()

        def _get_device(self):
            raise NotImplementedError()


class TestRealSwitchInterfaceProtocol(Bases.SwitchInterfaceProtocolTestBase):
    def _press_button(self):
        print('Press and hold the button on the test jig.')

    def _release_button(self):
        print('Release the button on the test jig.')

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


class TestFakeSwitchInterfaceProtocol(Bases.SwitchInterfaceProtocolTestBase):
    def _press_button(self):
        self.fake_switch_device.press_button()

    def _release_button(self):
        self.fake_switch_device.release_button()

    def _get_device(self):
        self.fake_switch_device = test.doubles.FakeSwitchDevice()
        return self.fake_switch_device