import time
from threading import Thread
from queue import Queue, Empty
from typing import Optional

from reactivex import Observable, Subject
from serial import Serial

from service.authorizer.gate.gate_controller import GateController


class SerialGateController(GateController):
    serial_port: str
    baud_rate: int
    timeout: int
    serial: Serial

    def __init__(
            self,
            serial_port: str = 'COM5',
            baud_rate: int = 9600,
            timeout: int = 1,
    ):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial = Serial(serial_port, baud_rate, timeout=timeout)

        self.running = True
        self.command_queue = Queue()
        self.response_queue = Queue()
        self.serial_thread = Thread(target=self.serial_communication)
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def serial_communication(self):
        while self.running:
            try:
                command = self.command_queue.get(timeout=0.1)
                self.serial.write((command + '\n').encode())
                print(f'Sent to Arduino: {command}')
            except Empty:
                pass

            if self.serial.in_waiting > 0:
                response = self.serial.readline().decode().strip()
                print(f'Received from Arduino: {response}')
                self.response_queue.put(response)
            time.sleep(0.1)

    def send_command(self, command: str):
        self.command_queue.put(command)

    def read_response(self) -> Optional[str]:
        try:
            response = self.response_queue.get_nowait()
            return response
        except Empty:
            return None

    def open_gate(self) -> Observable[bool]:
        self.send_command('Entrance Gate Open')
        vehicle_passed = Subject[bool]()
        thread = Thread(target=self.observe_vehicle_passed, args=(vehicle_passed,))
        thread.daemon = True
        thread.start()
        return vehicle_passed

    def observe_vehicle_passed(self, subject: Subject[bool]):
        while self.running:
            response = self.read_response()
            if response == "Car Entered":
                subject.on_next(True)
                break

            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.serial.close()
