from reactivex import Observable, Subject

from service.authorizer.gate.gate_controller import GateController


class PrintingGateController(GateController):
    def open_gate(self) -> Observable[bool]:
        print('Gate is open!')
        vehicle_passed = Subject[bool]()
        vehicle_passed.on_next(True)
        return vehicle_passed
