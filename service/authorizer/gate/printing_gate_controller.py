import asyncio
from threading import Timer

from reactivex import Observable, Subject

from service.authorizer.gate.gate_controller import GateController


def on_vehicle_passed(subject: Subject[bool]):
    subject.on_next(True)
    print('Car passed')


class PrintingGateController(GateController):
    def open_gate(self) -> Observable[bool]:
        print('Gate is open!')
        vehicle_passed = Subject[bool]()
        Timer(10, on_vehicle_passed, args=(vehicle_passed, )).start()
        return vehicle_passed
