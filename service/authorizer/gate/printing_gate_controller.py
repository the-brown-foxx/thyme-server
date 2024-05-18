from service.authorizer.gate.gate_controller import GateController


class PrintingGateController(GateController):
    def open_gate(self):
        print('Gate is open!')
