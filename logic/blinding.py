from hardware.actuators.servo import Servo
from observer_pattern.observer import Observer
from hardware.sensors.raw_analog import RawAnalog


class Blinding(Observer):
    def __init__(self, servo: Servo, lower_state: int, higher_state: int,
                 trigger: int = None, sensor: RawAnalog = None,
                 trigger_val: int = None, hister_val: int = 100):
        self.servo: Servo = servo
        self.trigger: int = trigger
        self.sensor = sensor
        self.trigger_val = trigger_val
        self.hister_val = hister_val
        self.lower_state = lower_state
        self.higher_state = higher_state
        servo.set_state(self.lower_state)
        self.triggered = False

    def update(self, *args):
        if self.trigger is not None and self.sensor is None:
            if args[0] == 1:
                self.__update_via_trigger()
        elif self.trigger is None and self.sensor is not None:
            self.__update_via_sensor()
        elif self.trigger is not None and self.sensor is not None:
            if isinstance(args[0], RawAnalog) and not self.triggered:
                self.__update_via_sensor()
            else:
                if args[0] == 1:
                    if self.triggered:
                        self.triggered = False
                        self.__update_via_sensor()
                    else:
                        self.triggered = True
                        self.__update_via_trigger()

    def __update_via_sensor(self):
        if self.servo.state == self.lower_state and self.sensor.sensor_value >= self.trigger_val + self.hister_val:
            self.servo.set_state(self.higher_state)
        elif self.servo.state == self.higher_state and self.sensor.sensor_value <= self.trigger_val - self.hister_val:
            self.servo.set_state(self.lower_state)

    def __update_via_trigger(self):
        if self.servo.state == self.lower_state:
            self.servo.set_state(self.higher_state)
        else:
            self.servo.set_state(self.lower_state)
