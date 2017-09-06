#! /usr/bin/env python3

# pylint: disable = no-self-use, attribute-defined-outside-init

import time

import tests.util
import tests.doubles

from yakserver import usbdevice


TIMEOUT = 0.1


class ACInterfaceV0_1_0ProtocolTest:
    # pylint: disable = no-member
    DEVICE_CLASS_ID = usbdevice.DeviceClassID(vendor_id=0x04d8,
                                              product_id=0x5901,
                                              release_number=0x0010)

    def setUp(self): # noqa
        super().setUp()
        self.channel_state = [False] * 4

    def test_turn_channel_on_and_off(self):
        self.device = self._get_device()
        self.device.connect()

        self.assertEqual(self.device.class_identifier, self.DEVICE_CLASS_ID)

        self._turn_channel_on(3)
        self._assert_channel_on(3)

        self._turn_channel_off(3)
        self._assert_channel_off(3)

    def _turn_channel_on(self, channel_number):
        self.channel_state[channel_number] = True
        self._send_state()

    def _turn_channel_off(self, channel_number):
        self.channel_state[channel_number] = False
        self._send_state()

    def _send_state(self):
        self.device.write(b'\x00' + self._channel_data())

    def _channel_data(self):
        channels_on = (i for i, state in enumerate(self.channel_state)
                       if state)
        data = sum(2 ** i for i in channels_on)
        return bytes([data])

    def _assert_channel_on(self, channel_number):
        raise NotImplementedError()

    def _assert_channel_off(self, channel_number):
        raise NotImplementedError()

    def _get_device(self):
        raise NotImplementedError()


class TestRealACInterfaceV0_1_0Protocol(ACInterfaceV0_1_0ProtocolTest,
                                        tests.util.RealDeviceTest):
    def _assert_channel_on(self, channel_number):
        self.assertEqual(channel_number, 3,
                         'Only channel 3 is supported for now')
        self.assertTrue(self._ask('Is the green LED on (Y/n)? '))

    def _assert_channel_off(self, channel_number):
        self.assertEqual(channel_number, 3,
                         'Only channel 3 is supported for now')
        self.assertFalse(self._ask('Is the green LED on (Y/n)? '))

    def _ask(self, message):
        response = input(message).lower()
        if not response or response == 'y':
            return True
        if response == 'n':
            return False
        raise ValueError("Expected 'y' or 'n'.")

    def _get_device(self):
        devices = self._find_devices()
        return devices[0]

    def _find_devices(self):
        return usbdevice.find_by_class_id(self.DEVICE_CLASS_ID)


class TestFakeACInterfaceV0_1_0Protocol(ACInterfaceV0_1_0ProtocolTest,
                                        tests.util.FakeDeviceTest):
    def _assert_channel_on(self, channel_number):
        self.assertTrue(self.device.channel_state[channel_number])

    def _assert_channel_off(self, channel_number):
        self.assertFalse(self.device.channel_state[channel_number])

    def _get_device(self):
        self.fake_device = tests.doubles.FakeACDeviceV0_1_0()
        return self.fake_device


class ACInterfaceV0_0_0ProtocolTest:
    # pylint: disable = no-member
    DEVICE_CLASS_ID = usbdevice.DeviceClassID(vendor_id=0x04d8,
                                              product_id=0x5901,
                                              release_number=0x0001)

    def test_turn_channel_on_and_off(self):
        self.device = self._get_device()
        self.device.connect()

        self.assertEqual(self.device.class_identifier, self.DEVICE_CLASS_ID)

        self._turn_channel_on()
        self._assert_channel_on()

        self._turn_channel_off()
        self._assert_channel_off()

    def _turn_channel_on(self):
        self.device.write(b'\x01')

    def _turn_channel_off(self):
        self.device.write(b'\x00')

    def _assert_channel_on(self):
        raise NotImplementedError()

    def _assert_channel_off(self):
        raise NotImplementedError()

    def _get_device(self):
        raise NotImplementedError()


class TestRealACInterfaceV0_0_0Protocol(ACInterfaceV0_0_0ProtocolTest,
                                        tests.util.RealDeviceTest):
    def _assert_channel_on(self):
        self.assertTrue(self._ask('Is the green LED on (Y/n)? '))

    def _assert_channel_off(self):
        self.assertFalse(self._ask('Is the green LED on (Y/n)? '))

    def _ask(self, message):
        response = input(message).lower()
        if not response or response == 'y':
            return True
        if response == 'n':
            return False
        raise ValueError("Expected 'y' or 'n'.")

    def _get_device(self):
        devices = self._find_devices()
        if not devices:
            print('Please plugin the device.')
        while not devices:
            time.sleep(0.1)
            devices = self._find_devices()
        return devices[0]

    def _find_devices(self):
        return usbdevice.find_by_class_id(self.DEVICE_CLASS_ID)


class TestFakeACInterfaceV0_0_0Protocol(ACInterfaceV0_0_0ProtocolTest,
                                        tests.util.FakeDeviceTest):
    def _assert_channel_on(self):
        self.assertTrue(self.device.channel_state)

    def _assert_channel_off(self):
        self.assertFalse(self.device.channel_state)

    def _get_device(self):
        self.fake_device = tests.doubles.FakeACDeviceV0_0_0()
        return self.fake_device
