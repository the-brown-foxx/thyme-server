import asyncio
from threading import Timer

from reactivex import Observable, Subject

from service.authorizer.gate.gate_controller import GateController


def on_vehicle_passed(subject: Subject[bool]):
    subject.on_next(True)
    print('Car passed')


class PrintingGateController(GateController):
    def __init__(self, entrance: bool):
        self.entrance = entrance

    def open_gate(self) -> Observable[bool]:
        gate = 'Entrance' if self.entrance else 'Exit'
        print(f'{gate} gate is open!')
        vehicle_passed = Subject[bool]()
        Timer(10, on_vehicle_passed, args=(vehicle_passed, )).start()
        return vehicle_passed
