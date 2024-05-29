import serial
import time
import threading
from queue import Queue, Empty
from typing import Union
from service.authorizer.access.parking_access_control import ParkingAccessControl
from service.authorizer.display.display_controller import DisplayController
from service.authorizer.gate.gate_controller import GateController
from service.authorizer.log.car_logger import CarLogger
from service.authorizer.monitor.car.car_monitor import CarMonitor
from service.authorizer.parking.parking_space_counter import ParkingSpaceCounter
from service.registry.model.car import Car


class ParkingEntranceControl(ParkingAccessControl):
    car_monitor: CarMonitor
    gate_controller: GateController
    display_controller: DisplayController
    parking_space_counter: ParkingSpaceCounter
    car_logger: CarLogger

    def __init__(
            self,
            car_monitor: CarMonitor,
            gate_controller: GateController,
            display_controller: DisplayController,
            parking_space_counter: ParkingSpaceCounter,
            car_logger: CarLogger,
            serial_port: str = 'COM5',  # Update this to your Arduino's serial port
            baud_rate: int = 9600,
            timeout: int = 1,
    ):
        self.car_monitor = car_monitor
        self.gate_controller = gate_controller
        self.display_controller = display_controller
        self.parking_space_counter = parking_space_counter
        self.car_logger = car_logger

        # Initialize the serial connection to the Arduino
        self.ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
        time.sleep(2)  # Wait for Arduino to reset

        self.running = True
        self.command_queue = Queue()
        self.response_queue = Queue()
        self.serial_thread = threading.Thread(target=self.serial_communication)
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def serial_communication(self):
        while self.running:
            try:
                command = self.command_queue.get(timeout=0.1)
                self.ser.write((command + '\n').encode())
                print(f'Sent to Arduino: {command}')
            except Empty:
                pass

            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode().strip()
                print(f'Received from Arduino: {response}')
                self.response_queue.put(response)
            time.sleep(0.1)

    def send_command(self, command: str):
        self.command_queue.put(command)

    def read_response(self) -> str:
        try:
            response = self.response_queue.get_nowait()
            return response
        except Empty:
            return ""

    def on_car_detected(self, car_or_registration_id: Union[Car, str]):
        if isinstance(car_or_registration_id, Car):
            car = car_or_registration_id
            self.parking_space_counter.decrement_available_space()
            self.gate_controller.open_gate()
            self.display_controller.show_car_info(car)
            vacant_space = self.parking_space_counter.get_parking_space_count().vacant_space
            self.display_controller.update_vacant_space(vacant_space)
            self.car_logger.log(car_registration_id=car.registration_id, entering=True)

            # Send command to Arduino to open the entrance gate
            self.send_command("Entrance Gate Open")

            # Wait for Arduino to signal that the car has passed
            while True:
                response = self.read_response()
                if response == "Car Entered":
                    self.car_monitor.mark_car_as_passed()
                    break
                time.sleep(0.1)  # Small delay to prevent high CPU usage
        elif isinstance(car_or_registration_id, str):
            registration_id = car_or_registration_id
            self.display_controller.show_unauthorized_message(registration_id)

    def start(self):
        (self.car_monitor.get_car_stream()
         .subscribe(lambda registration_id: self.on_car_detected(registration_id)))
        vacant_space = self.parking_space_counter.get_parking_space_count().vacant_space
        self.display_controller.update_vacant_space(vacant_space)

    def stop(self):
        self.running = False
        self.ser.close()

