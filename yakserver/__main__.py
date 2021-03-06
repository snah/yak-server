#! /usr/bin/env python3

"""The yakserver application."""

from yakserver import interface
from yakserver import events


class Application:
    """Object holding the main application state and main loop."""

    def __init__(self):
        """Create the application object."""
        self.switch_interface = None
        self.ac_interface = None

    def setup(self):
        """Initialize the application in preparation for the main loop."""
        interface_manager = interface.InterfaceManager()
        self.switch_interface = interface_manager.input_interfaces()[0]
        self.switch_interface.initialize()

        self.ac_interface = interface_manager.output_interfaces()[0]
        self.ac_interface.initialize()

    def main_loop(self):
        """Run the program untill the server stops."""
        while self.server_running():
            self.main_loop_iteration()

    @staticmethod
    def server_running():
        """Return True if the server is running, False otherwise."""
        return True

    def main_loop_iteration(self):
        """Execute one iteration of the main loop."""
        event = self.get_event()
        self.handle_event(event)

    def get_event(self):
        """Get the next event.

        If there is no event to be processed, block untill one becomes
        available.
        """
        return self.switch_interface.get_event()

    def handle_event(self, event):
        """Handle an event."""
        if event:
            if isinstance(event, events.ButtonDownEvent):
                self.ac_interface.send_command(events.LampOnEvent())
            elif isinstance(event, events.ButtonUpEvent):
                self.ac_interface.send_command(events.LampOffEvent())


def main():
    """Run the server."""
    application = Application()
    application.setup()
    application.main_loop()


if __name__ == '__main__':
    main()
