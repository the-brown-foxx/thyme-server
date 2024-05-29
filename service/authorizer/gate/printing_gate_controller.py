from threading import Timer

from reactivex import Observable, Subject

from service.authorizer.gate.gate_controller import GateController


class PrintingGateController(GateController):
    def open_gate(self) -> Observable[bool]:
        print('Gate is open!')
        vehicle_passed = Subject[bool]()
        timer = Timer(5, self.on_vehicle_passed, args=(vehicle_passed, ))
        timer.start()
        return vehicle_passed

    @staticmethod
    def on_vehicle_passed(subject: Subject[bool]):
        subject.on_next(True)
