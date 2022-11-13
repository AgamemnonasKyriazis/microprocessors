from numpy.random import randint

from CircuitModeling import Circuit, Element
from SignalProbabilities import OPS


def create_random_workload(N, size):
    """Creates a random workload of N size"""
    workload = []
    for _ in range(N):
        m = [randint(0, 2) for _ in range(size)]
        workload.append(m)
    return workload


class VirtualCircuitEmulator:

    def __init__(self, circuit: Circuit) -> None:
        self.circuit = circuit

    def process(self, element: Element):
        op = OPS[
            self.circuit.get_elements_type_table()[
                element.get_operation_index()
            ]
        ]
        element_inputs = [self.circuit.get_signals_table()[i] for i in element.get_inputs_indexes()]
        element_output = op(element_inputs)
        self.circuit.update_signal(element.get_output_index(), element_output)


    def simulate_circuit(self, inputs):
        for i in range(len(self.circuit.get_top_inputs_indexes())):
            signal_index = self.circuit.get_top_inputs_indexes()[i]
            self.circuit.update_signal(signal_index, inputs[i])
        for elem in self.circuit.get_elements_table():
            self.process(elem)
        return self.circuit.get_signals_table()


    def simulate_circuit_with_workload(self, N):
        size = len(self.circuit.get_top_inputs_indexes())
        workload = create_random_workload(N, size)
        switches_table = [0]*len(self.circuit.get_signals_table())
        for inputs in workload:
            old_signals_values = [sgn for sgn in self.circuit.get_signals_table()]
            new_signals_values = self.simulate_circuit(inputs)
            for elem in self.circuit.get_elements_table():
                i = elem.get_output_index()
                switches_table[i] += 1 if old_signals_values[i] != new_signals_values[i] else 0
        return list(map((lambda u: u/N), switches_table))
