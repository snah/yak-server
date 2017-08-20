#! /usr/bin/env python3

# pylint: disable = no-self-use, unused-argument

from tests import util

import yakserver.translators
import yakserver.events


class TestLookupTranslator(util.TestCase):
    class ConcreteLookupTranslator(yakserver.translators.LookupTranslator):
        DEVICE_CLASS_ID = None
        TRANSLATION_TABLE = yakserver.translators.LookupTable({
            b'a': yakserver.events.ButtonUpEvent,
            b'b': yakserver.events.ButtonDownEvent})

    def setUp(self):
        self.translator = self.ConcreteLookupTranslator()

    def test_translates_raw_data_to_event(self):
        event = self.translator.raw_data_to_event(b'b')

        self.assert_event_equal(event, yakserver.events.ButtonDownEvent())

    def test_raw_to_event_raises_value_error_on_unknown_input(self):
        with self.assertRaises(ValueError):
            self.translator.raw_data_to_event(b'\x11')

    def test_raw_to_event_raises_type_error_on_wrong_input_type(self):
        with self.assertRaises(TypeError):
            self.translator.raw_data_to_event(True)

    def test_translates_event_to_raw_data(self):
        event = yakserver.events.ButtonUpEvent()
        raw_data = self.translator.event_to_raw_data(event)

        self.assertEqual(raw_data, b'a')

    def test_event_to_raw_data_raises_value_error_on_unknown_event_type(self):
        with self.assertRaises(ValueError):
            self.translator.event_to_raw_data(yakserver.events.Event())

    def test_event_to_raw_data_raises_type_error_if_not_given_an_event(self):
        with self.assertRaises(TypeError):
            self.translator.event_to_raw_data('not an event')

    def test_correct_maximum_data_length(self):
        maximum_data_length = self.translator.maximum_data_length()

        self.assertEqual(maximum_data_length, 1)
